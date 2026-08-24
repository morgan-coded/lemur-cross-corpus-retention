#!/usr/bin/env python
"""
LEMUR portability pilot harness (txtai #1173).

One deterministic script, many small units. Every unit writes JSON atomically
(tmp + rename) and every reader validates JSON before trusting it, because a
power interruption once zeroed freshly written files.

Subcommands (all take --root, the pilot work dir):
  env            record environment + assert the pinned txtai checkout is the one imported
  prep-targets   stage BEIR corpora (corpus/queries/test qrels) + token-length stats
  prep-source    fetch the LightOn mixture documents (never scores/) and draw stratified samples
  train          train one LEMUR artifact (target corpus or source draw; mlp or elm)
  remean         target token-row mean of an UNCENTERED encode -> safetensors key center.mean
  recal          copy an artifact and rewrite lemur.mean/lemur.std from maxsim(target docs, sample)
  preflight      calibration distribution (maxsim(docs, sample) - mean) / std on target docs
  index-eval     one product-stage cell: index + search + pytrec_eval, per-query scores persisted
  summarize      RESULTS.md + summary.json from every completed cell (paired bootstrap)

Nothing here posts anywhere. Measurement only.
"""

import argparse
import csv
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from collections import defaultdict

COLBERT_REPO = "colbert-ir/colbertv2.0"
COLBERT_REV = "c1e84128e85ef755c096a95bdb06b47793b13acf"
TXTAI_PIN = "20f818f72cacbdc7ea01912788a4b988db029c5e"
LIGHTON_REPO = "lightonai/embeddings-fine-tuning"
LIGHTON_REV = "1ca463331ed637d25c1058567e932e0d3bad2983"
CONSTITUENTS = ["fever", "fiqa", "hotpotqa", "msmarco", "nq", "squadv2", "trivia"]
MEASURES = {"ndcg_cut.10", "map_cut.10", "recall.10", "P.10"}
METRIC_KEYS = ["ndcg_cut_10", "map_cut_10", "recall_10", "P_10"]
IVF_THRESHOLD = 5000  # txtai faiss switches to IVF above this many rows

# Held fixed in every training arm and recorded in the run manifest.
# trainsubsetsize is deliberately NOT pinned: the library default (8192) is constitutive.
FIT_FIXED = {
    "learnsubsetsize": 100000,
    "olssamplesize": 16384,
    "layers": 1,
    "hiddendim": 512,
    "finalhiddendim": 2048,
    "activation": "gelu",
    "queryscale": 32,
    "lr": 3e-3,
    "batchsize": 512,
    "gradclip": 0.5,
}
MLP_EPOCHS, ELM_EPOCHS = 100, 0
MLP_VALIDATION, ELM_VALIDATION = 0.1, 0.0


# ----------------------------------------------------------------------------- io helpers


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, obj):
    """Atomic JSON write: tmp file in the same dir, fsync, rename."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=os.path.dirname(os.path.abspath(path)))
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def read_json(path, required=True):
    """Validated JSON read: a zeroed/truncated file raises instead of silently passing."""
    if not os.path.exists(path):
        if required:
            raise FileNotFoundError(path)
        return None
    with open(path, "rb") as f:
        raw = f.read()
    if not raw.strip() or raw.count(b"\x00") > 0:
        raise ValueError(f"corrupt JSON (empty or NUL bytes): {path}")
    return json.loads(raw.decode("utf-8"))


def write_jsonl(path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=os.path.dirname(os.path.abspath(path)))
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def read_jsonl(path):
    rows = []
    with open(path, "rb") as f:
        raw = f.read()
    if raw.count(b"\x00") > 0:
        raise ValueError(f"corrupt JSONL (NUL bytes): {path}")
    for line in raw.decode("utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def beir_text(row):
    """benchmarks.py text rule: 'title. text' when a title exists."""
    return f'{row["title"]}. {row["text"]}' if row.get("title") else row["text"]


def load_corpus(root, corpus):
    path = os.path.join(root, "data", "targets", corpus, "corpus.jsonl")
    ids, texts = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            text = beir_text(row)
            if text:
                ids.append(row["_id"])
                texts.append(text)
    return ids, texts


def load_qrels(root, corpus):
    rel = {}
    path = os.path.join(root, "data", "targets", corpus, "qrels", "test.tsv")
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        next(reader)
        for row in reader:
            qid, did, score = row[0], row[1], int(row[2])
            rel.setdefault(qid, {})[did] = score
    return rel


def load_queries(root, corpus, restrict=None):
    path = os.path.join(root, "data", "targets", corpus, "queries.jsonl")
    uids, queries = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            if restrict is None or row["_id"] in restrict:
                uids.append(row["_id"])
                queries.append(row["text"])
    return uids, queries


def colbert_path(args):
    """Local ColBERTv2 snapshot at the pinned revision, loaded by path (Download() cannot pin)."""
    if args.model_path:
        return args.model_path
    from huggingface_hub import snapshot_download

    return snapshot_download(COLBERT_REPO, revision=COLBERT_REV, local_files_only=not args.allow_download)


def cuda_stats():
    try:
        import torch

        if torch.cuda.is_available():
            return {
                "max_allocated_gb": round(torch.cuda.max_memory_allocated() / 1e9, 3),
                "max_reserved_gb": round(torch.cuda.max_memory_reserved() / 1e9, 3),
            }
    except Exception:  # pylint: disable=W0718
        pass
    return {}


def device_args(args):
    return not args.cpu


# ----------------------------------------------------------------------------- env


def cmd_env(args):
    import faiss
    import numpy
    import pytrec_eval
    import torch
    import txtai

    info = {
        "time": now(),
        "python": sys.version.split()[0],
        "txtai_file": os.path.abspath(txtai.__file__),
        "torch": torch.__version__,
        "faiss": faiss.__version__,
        "numpy": numpy.__version__,
        "pytrec_eval": getattr(pytrec_eval, "__version__", "?"),
        "cuda": torch.cuda.is_available(),
        "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "txtai_pin_expected": TXTAI_PIN,
    }
    if args.checkout:
        head = subprocess.run(["git", "-C", args.checkout, "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        info["txtai_head"] = head
        info["txtai_head_matches_pin"] = head == TXTAI_PIN
        expected = os.path.abspath(os.path.join(args.checkout, "src", "python", "txtai"))
        info["txtai_imported_from_checkout"] = info["txtai_file"].startswith(expected)
        if not info["txtai_head_matches_pin"] or not info["txtai_imported_from_checkout"]:
            write_json(os.path.join(args.root, "env.json"), info)
            raise SystemExit(f"ENV STOP: txtai pin/import mismatch: {info}")
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=power.limit,memory.used,memory.total", "--format=csv,noheader"], capture_output=True, text=True, check=False)
        info["nvidia_smi"] = out.stdout.strip()
    except FileNotFoundError:
        info["nvidia_smi"] = "n/a"
    info["colbert_path"] = colbert_path(args)
    info["colbert_rev"] = COLBERT_REV
    write_json(os.path.join(args.root, "env.json"), info)
    print(json.dumps(info, indent=2))


# ----------------------------------------------------------------------------- prep-targets


def cmd_prep_targets(args):
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(colbert_path(args))
    stats = {}
    for corpus in args.corpora.split(","):
        src = os.path.join(args.beir, corpus)
        dst = os.path.join(args.root, "data", "targets", corpus)
        os.makedirs(os.path.join(dst, "qrels"), exist_ok=True)
        rows = []
        with open(os.path.join(src, "corpus.jsonl"), encoding="utf-8") as f:
            for line in f:
                rows.append(json.loads(line))
        if args.mini:
            rows = rows[: args.mini]
        keep = {r["_id"] for r in rows}
        with open(os.path.join(dst, "corpus.jsonl"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        # qrels restricted to staged docs (identity unless --mini)
        qrels = {}
        with open(os.path.join(src, "qrels", "test.tsv"), encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            header = next(reader)
            for row in reader:
                if row[1] in keep:
                    qrels.setdefault(row[0], []).append(row)
        with open(os.path.join(dst, "qrels", "test.tsv"), "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(header)
            for q in qrels.values():
                for row in q:
                    w.writerow(row)
        nq = 0
        with open(os.path.join(src, "queries.jsonl"), encoding="utf-8") as f, open(os.path.join(dst, "queries.jsonl"), "w", encoding="utf-8") as out:
            for line in f:
                row = json.loads(line)
                if row["_id"] in qrels:
                    out.write(json.dumps(row) + "\n")
                    nq += 1
        # token-length characterization (raw ColBERT tokenizer counts, no truncation)
        lengths = []
        for r in rows:
            text = beir_text(r)
            if text:
                lengths.append(len(tokenizer(text, add_special_tokens=True)["input_ids"]))
        import numpy as np

        arr = np.asarray(lengths, dtype=np.float64)
        stats[corpus] = {
            "docs": len(rows),
            "queries_in_test_qrels": nq,
            "qrels_rows": sum(len(v) for v in qrels.values()),
            "qrels_sha256": sha256_file(os.path.join(dst, "qrels", "test.tsv")),
            "corpus_sha256": sha256_file(os.path.join(dst, "corpus.jsonl")),
            "ann_default": "IVF" if len(rows) > IVF_THRESHOLD else "exact",
            "tokens": {
                "mean": round(float(arr.mean()), 2),
                "median": float(np.median(arr)),
                "p95": float(np.percentile(arr, 95)),
                "p99": float(np.percentile(arr, 99)),
                "cv": round(float(arr.std() / arr.mean()), 4),
                "frac_over_180": round(float((arr > 180).mean()), 4),
            },
        }
        print(corpus, json.dumps(stats[corpus]))
    write_json(os.path.join(args.root, "data", "targets", "stats.json"), stats)


# ----------------------------------------------------------------------------- prep-source


def normalize_text(text):
    return " ".join(text.lower().split())


def shingles(text, n=5):
    words = normalize_text(text).split()
    if len(words) < n:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i : i + n]) for i in range(len(words) - n + 1)}


def minhash(shingle_set, perms):
    """64-permutation MinHash via (a*x+b) mod prime over sha1-hashed shingles."""
    prime = (1 << 61) - 1
    values = [int(hashlib.sha1(s.encode("utf-8")).hexdigest()[:15], 16) for s in shingle_set]
    if not values:
        return [0] * len(perms)
    return [min(((a * v + b) % prime) for v in values) for a, b in perms]


def near_duplicate_audit(texts, seed=7, bands=8, rows=8):
    """Exact-normalized duplicates plus MinHash/LSH candidates with estimated Jaccard >= 0.8."""
    rng = random.Random(seed)
    perms = [(rng.randrange(1, 1 << 60), rng.randrange(0, 1 << 60)) for _ in range(bands * rows)]
    norm = [normalize_text(t) for t in texts]
    exact = defaultdict(list)
    for i, n in enumerate(norm):
        exact[hashlib.sha1(n.encode("utf-8")).hexdigest()].append(i)
    exact_groups = [g for g in exact.values() if len(g) > 1]
    sets = [shingles(t) for t in texts]
    sigs = [minhash(s, perms) for s in sets]
    buckets = defaultdict(list)
    for i, sig in enumerate(sigs):
        for b in range(bands):
            key = (b, tuple(sig[b * rows : (b + 1) * rows]))
            buckets[key].append(i)
    candidates = set()
    for members in buckets.values():
        if len(members) > 1:
            for x in range(len(members)):
                for y in range(x + 1, len(members)):
                    candidates.add((members[x], members[y]))
    near = []
    for i, j in sorted(candidates):
        inter = len(sets[i] & sets[j])
        union = len(sets[i] | sets[j]) or 1
        jac = inter / union
        if jac >= 0.8:
            near.append((i, j, round(jac, 4)))
    return {"exact_duplicate_groups": len(exact_groups), "exact_duplicate_docs": sum(len(g) - 1 for g in exact_groups), "near_duplicate_pairs_j08": len(near), "near_pairs": near[:200]}


def cmd_prep_source(args):
    import pyarrow.parquet as pq

    if args.from_beir:
        # smoke-only path: a BEIR corpus standing in for the mixture
        ids, texts = load_corpus(args.root, args.from_beir)
        rng = random.Random(f"{args.seed}:{args.from_beir}")
        idx = sorted(rng.sample(range(len(texts)), min(args.total, len(texts))))
        rows = [{"id": f"{args.from_beir}:{ids[i]}", "constituent": args.from_beir, "text": texts[i]} for i in idx]
        manifest = {"name": args.name, "smoke_only_source": args.from_beir, "seed": args.seed, "total_requested": args.total, "drawn": len(rows)}
    else:
        if args.hf_dir:
            hfdir = args.hf_dir
        else:
            from huggingface_hub import snapshot_download

            hfdir = snapshot_download(LIGHTON_REPO, repo_type="dataset", revision=LIGHTON_REV, allow_patterns=["documents/*.parquet"], max_workers=4)
        docdir = os.path.join(hfdir, "documents")
        constituents = args.constituents.split(",")
        quota, rem = divmod(args.total, len(constituents))
        rows, manifest = [], {"name": args.name, "repo": LIGHTON_REPO, "revision": LIGHTON_REV, "seed": args.seed, "total_requested": args.total, "method": "stratified-equal-per-constituent; uniform row sample within constituent over all shards (parquet row-group metadata); per-constituent seed = sha512(f'{seed}:{constituent}')", "constituents": {}}
        for ci, name in enumerate(sorted(constituents)):
            k = quota + (1 if ci < rem else 0)
            shards = sorted(f for f in os.listdir(docdir) if f.startswith(f"{name}-") and f.endswith(".parquet"))
            if not shards:
                raise SystemExit(f"no shards for constituent {name} under {docdir}")
            # row-group map without loading data
            groups = []  # (shard, rowgroup, nrows)
            for shard in shards:
                meta = pq.ParquetFile(os.path.join(docdir, shard)).metadata
                for g in range(meta.num_row_groups):
                    groups.append((shard, g, meta.row_group(g).num_rows))
            total = sum(n for _, _, n in groups)
            rng = random.Random(f"{args.seed}:{name}")
            picks = sorted(rng.sample(range(total), min(k, total)))
            # map global indices to (group, offset)
            drawn, pi, base = [], 0, 0
            for shard, g, n in groups:
                local = []
                while pi < len(picks) and picks[pi] < base + n:
                    local.append(picks[pi] - base)
                    pi += 1
                if local:
                    table = pq.ParquetFile(os.path.join(docdir, shard)).read_row_group(g, columns=["document_id", "document"])
                    dids, docs = table.column("document_id").to_pylist(), table.column("document").to_pylist()
                    for off in local:
                        text = docs[off] if docs[off] else ""
                        if text.strip():
                            drawn.append({"id": f"{name}:{dids[off]}", "constituent": name, "text": text, "shard": shard, "rowgroup": g, "offset": off})
                base += n
                if pi >= len(picks):
                    break
            manifest["constituents"][name] = {"shards": len(shards), "total_rows": total, "quota": k, "drawn": len(drawn), "empty_dropped": k - len(drawn)}
            rows.extend(drawn)
            print(name, manifest["constituents"][name])
    audit = near_duplicate_audit([r["text"] for r in rows])
    manifest["near_duplicate_audit"] = audit
    manifest["drawn_total"] = len(rows)
    manifest["ids_sha256"] = sha256_bytes("\n".join(r["id"] for r in rows).encode("utf-8"))
    out = os.path.join(args.root, "data", "source", f"{args.name}.jsonl")
    write_jsonl(out, rows)
    write_json(os.path.join(args.root, "data", "source", f"{args.name}.manifest.json"), manifest)
    print(json.dumps({k: v for k, v in manifest.items() if k != "near_duplicate_audit"}, indent=2), json.dumps({k: v for k, v in audit.items() if k != "near_pairs"}))


# ----------------------------------------------------------------------------- train


def resolve_data(args):
    """Returns (label, ids, texts) for target:<corpus> or source:<draw>."""
    kind, name = args.data.split(":", 1)
    if kind == "target":
        ids, texts = load_corpus(args.root, name)
        return name, ids, texts
    if kind == "source":
        rows = read_jsonl(os.path.join(args.root, "data", "source", f"{name}.jsonl"))
        return name, [r["id"] for r in rows], [r["text"] for r in rows]
    raise SystemExit("--data must be target:<corpus> or source:<draw>")


def artifact_report(outdir):
    """Keys, calibration stats, sample rank/condition, center checksum — read from the saved artifact."""
    import numpy as np
    import torch
    from safetensors import safe_open

    report = {}
    with safe_open(os.path.join(outdir, "model.safetensors"), framework="pt", device="cpu") as src:
        keys = list(src.keys())
        report["keys"] = sorted(keys)
        report["lemur_mean"] = float(src.get_tensor("lemur.mean")[0])
        report["lemur_std"] = float(src.get_tensor("lemur.std")[0])
        sample = src.get_tensor("lemur.sample")
        report["sample_shape"] = list(sample.shape)
        if "lemur.center" in keys:
            center = src.get_tensor("lemur.center")
            report["center_sha256"] = sha256_bytes(center.numpy().astype(np.float32).tobytes())
            report["center_norm"] = float(torch.linalg.norm(center))
        else:
            report["center_sha256"] = None
    # rank / condition number of the stored sample at the lemur.py:117 tolerance rule
    values = torch.linalg.svdvals(sample.to(torch.float32))
    tol = torch.finfo(values.dtype).eps * max(sample.shape) * values.max()
    surviving = int((values > tol).sum())
    report["sample_rank_at_tolerance"] = surviving
    report["sample_condition_number"] = float(values.max() / values[surviving - 1]) if surviving else None
    report["config"] = read_json(os.path.join(outdir, "config.json"))
    return report


def cmd_train(args):
    import torch
    from txtai.pipeline import LemurTrainer

    label, ids, texts = resolve_data(args)
    outdir = os.path.join(args.root, "artifacts", args.artifact)
    if os.path.exists(os.path.join(outdir, "train.json")):
        print("exists:", outdir)
        return
    vectors = {"center": False} if args.center_false else None
    epochs = MLP_EPOCHS if args.modeltype == "mlp" else ELM_EPOCHS
    validation = MLP_VALIDATION if args.modeltype == "mlp" else ELM_VALIDATION
    corpussubsetsize = args.corpussubsetsize or len(texts)
    if corpussubsetsize < len(texts):
        # the draw must be explicit and recorded, never the trainer's own resample
        raise SystemExit("corpussubsetsize smaller than the data list: draw the subset offline and pass it as data")
    params = {"epochs": epochs, "seed": args.seed, "validationsplit": validation, "learn": None, "learncategory": "query", "corpussubsetsize": corpussubsetsize, "gpu": device_args(args), "vectors": vectors, **FIT_FIXED}
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    start = time.time()
    lemur = LemurTrainer()(colbert_path(args), texts, outdir, gpu=params["gpu"], vectors=vectors, learn=None, learncategory="query", corpussubsetsize=corpussubsetsize, validationsplit=validation, epochs=epochs, seed=args.seed, **FIT_FIXED)
    wall = round(time.time() - start, 1)
    report = {
        "artifact": args.artifact,
        "data": args.data,
        "data_label": label,
        "n_texts": len(texts),
        "ids_sha256": sha256_bytes("\n".join(ids).encode("utf-8")),
        "modeltype": args.modeltype,
        "seed": args.seed,
        "params": {k: v for k, v in params.items() if k != "vectors"},
        "center_configured": vectors is not None,
        "trainsubsetsize_default_used": 8192,
        "selectedepoch": lemur.selectedepoch,
        "selectedloss": lemur.selectedloss,
        "selectionmetric": lemur.selectionmetric,
        "wall_seconds": wall,
        "cuda": cuda_stats(),
        "time": now(),
        "artifact_report": artifact_report(outdir),
    }
    write_json(os.path.join(outdir, "train.json"), report)
    print(json.dumps({k: report[k] for k in ["artifact", "n_texts", "modeltype", "seed", "selectedepoch", "selectedloss", "wall_seconds", "cuda"]}))


# ----------------------------------------------------------------------------- token encodes (remean / recal / preflight)


def make_pooling(args, center):
    """A LatePooling with no fixed-dimensional encoder: raw (optionally centered) multi-vectors."""
    from txtai.models import Models, PoolingFactory

    deviceid = Models.deviceid(device_args(args))
    modelargs = {"muvera": None, "lemur": None, "center": center}
    return PoolingFactory.create({"method": None, "path": colbert_path(args), "device": deviceid, "tokenizer": None, "maxlength": None, "modelargs": modelargs})


def encode_tokens(pooling, texts, batch=32):
    """Yields unpadded per-document token matrices (numpy)."""
    import numpy as np

    for start in range(0, len(texts), batch):
        out = pooling.encode(texts[start : start + batch], batch=batch, category="data")
        for doc in out:
            mask = np.any(doc != 0, axis=1)
            yield doc[mask]


def load_lemur(args, artifact):
    import torch
    from txtai.models.pooling.lemur import Lemur

    device = "cuda" if (device_args(args) and torch.cuda.is_available()) else "cpu"
    return Lemur(path=os.path.join(args.root, "artifacts", artifact), device=device)


def sample_docs(args, corpus, n, seed):
    ids, texts = load_corpus(args.root, corpus)
    if n and n < len(texts):
        rng = random.Random(f"{seed}:{corpus}:docsample")
        idx = sorted(rng.sample(range(len(texts)), n))
        return [ids[i] for i in idx], [texts[i] for i in idx]
    return ids, texts


def cmd_remean(args):
    import numpy as np
    from safetensors.numpy import save_file

    ids, texts = load_corpus(args.root, args.corpus)
    pooling = make_pooling(args, center=False)
    total, count = None, 0
    for doc in encode_tokens(pooling, texts):
        s = doc.sum(axis=0, dtype=np.float64)
        total = s if total is None else total + s
        count += doc.shape[0]
    mean = (total / count).astype(np.float32)
    out = os.path.join(args.root, "means", f"{args.corpus}.safetensors")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    save_file({"center.mean": mean}, out)
    info = {"corpus": args.corpus, "n_docs": len(ids), "n_tokens": count, "mean_sha256": sha256_bytes(mean.tobytes()), "mean_norm": float(np.linalg.norm(mean)), "path": out, "time": now(), "uncentered_encode": True}
    write_json(os.path.join(args.root, "means", f"{args.corpus}.json"), info)
    print(json.dumps(info))


def calibration_matrix(args, lemur, corpus, n, seed):
    """maxsim(target docs centered with the artifact's own mean, stored sample) as a (sample x docs) tensor."""
    import numpy as np
    import torch

    center = {"scope": "collection", "mean": lemur.center.detach().cpu().numpy()} if lemur.center is not None else False
    pooling = make_pooling(args, center=center)
    ids, texts = sample_docs(args, corpus, n, seed)
    sample = lemur.sample.to(lemur.device)
    cols = []
    for doc in encode_tokens(pooling, texts):
        d = torch.from_numpy(np.ascontiguousarray(doc)).to(lemur.device, dtype=torch.float32)
        cols.append((sample @ d.T).max(dim=1).values)
    matrix = torch.stack(cols, dim=1)
    return ids, matrix, center


def cmd_recal(args):
    import torch
    from safetensors.torch import load_file, save_file

    lemur = load_lemur(args, args.artifact)
    ids, matrix, center = calibration_matrix(args, lemur, args.corpus, args.n, args.seed)
    newmean, newstd = matrix.mean(), matrix.std(unbiased=False)
    src = os.path.join(args.root, "artifacts", args.artifact)
    dst = os.path.join(args.root, "artifacts", args.out)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("train.json"))
    tensors = load_file(os.path.join(dst, "model.safetensors"))
    tensors["lemur.mean"] = newmean.detach().cpu().reshape(1).to(torch.float32)
    tensors["lemur.std"] = newstd.detach().cpu().reshape(1).to(torch.float32)
    save_file(tensors, os.path.join(dst, "model.safetensors"))
    info = {"artifact": args.out, "source_artifact": args.artifact, "corpus": args.corpus, "n_docs": len(ids), "docs_sha256": sha256_bytes("\n".join(ids).encode("utf-8")), "old_mean": float(lemur.mean), "old_std": float(lemur.std), "new_mean": float(newmean), "new_std": float(newstd), "centered_with": "artifact lemur.center (mu_S)" if center else "none", "rewrote_only": ["lemur.mean", "lemur.std"], "time": now()}
    write_json(os.path.join(dst, "recal.json"), info)
    print(json.dumps(info))


def cmd_preflight(args):
    import numpy as np

    lemur = load_lemur(args, args.artifact)
    ids, matrix, center = calibration_matrix(args, lemur, args.corpus, args.n, args.seed)
    z = ((matrix - lemur.mean) / lemur.std).detach().cpu().numpy().ravel()
    pct = {f"p{p}": float(np.percentile(z, p)) for p in (1, 5, 25, 50, 75, 95, 99)}
    info = {"artifact": args.artifact, "corpus": args.corpus, "n_docs": len(ids), "n_values": int(z.size), "mean": float(z.mean()), "sd": float(z.std()), **pct, "frac_below_zero": float((z < 0).mean()), "frac_below_minus2": float((z < -2).mean()), "artifact_mean": float(lemur.mean), "artifact_std": float(lemur.std), "centered_with": "artifact lemur.center (mu_S)" if center else "none", "time": now()}
    write_json(os.path.join(args.root, "preflight", f"{args.artifact}--{args.corpus}.json"), info)
    print(json.dumps(info))


# ----------------------------------------------------------------------------- index-eval


def cmd_index_eval(args):
    import numpy as np
    import pytrec_eval
    from txtai.embeddings import Embeddings

    cellpath = os.path.join(args.root, "cells", f"{args.cell}.json")
    if os.path.exists(cellpath):
        print("exists:", cellpath)
        return
    vectors = {}
    if args.artifact.startswith("muvera:"):
        reps, hashes, proj = args.artifact.split(":", 1)[1].split(",")
        vectors["muvera"] = {"repetitions": int(reps), "hashes": int(hashes), "projection": int(proj)}
        encoder_desc = f"muvera r{reps} h{hashes} p{proj} = {int(reps) * (2 ** int(hashes)) * int(proj)} dims"
    else:
        vectors["lemur"] = {"path": os.path.join(args.root, "artifacts", args.artifact)}
        encoder_desc = f"lemur {args.artifact}"
    if args.variant == "remean":
        vectors["center"] = {"scope": "collection", "path": os.path.join(args.root, "means", f"{args.corpus}.safetensors")}
    elif args.variant == "legacy":
        vectors["center"] = False
    config = {"path": colbert_path(args), "backend": "faiss", "vectors": vectors, "gpu": device_args(args)}
    if args.ann == "exact":
        config["faiss"] = {"components": "IDMap,Flat"}
    ids, texts = load_corpus(args.root, args.corpus)
    qrels = load_qrels(args.root, args.corpus)
    uids, queries = load_queries(args.root, args.corpus, restrict=set(qrels))

    embeddings = Embeddings(config)
    start = time.time()
    embeddings.index((i, t, None) for i, t in zip(ids, texts))
    indextime = round(time.time() - start, 2)
    pooling = embeddings.model.model
    resolved = getattr(pooling, "center", None)
    center_info = None
    if isinstance(resolved, dict):
        center_info = {"scope": resolved["scope"]}
        if resolved["scope"] == "collection":
            center_info["mean_sha256"] = sha256_bytes(np.asarray(resolved["mean"], dtype=np.float32).tobytes())
    encoder = getattr(pooling, "encoder", None)
    ann = embeddings.ann
    components, index_desc = None, None
    try:
        cfg = ann.config if isinstance(ann.config, dict) else {}
        raw = cfg.get("faiss", {}).get("components")
        components = raw if isinstance(raw, str) else (str(raw) if raw is not None else None)
        build = cfg.get("build") or cfg.get("metadata") or {}
        if isinstance(build, dict) and isinstance(build.get("components"), str):
            components = components or build["components"]
    except Exception:  # pylint: disable=W0718
        pass
    def describe_index():
        """Live faiss index type (+ nlist/nprobe); call AFTER search — txtai sets nprobe at search time."""
        try:
            import faiss

            idx = faiss.downcast_index(ann.backend)
            desc = type(idx).__name__
            inner = getattr(idx, "index", None)
            if inner is not None:
                inner = faiss.downcast_index(inner)
                desc += f"({type(inner).__name__}" + (f" nlist={inner.nlist} nprobe={inner.nprobe}" if hasattr(inner, "nlist") else "") + ")"
            elif hasattr(idx, "nlist"):
                desc += f" nlist={idx.nlist} nprobe={idx.nprobe}"
            return desc
        except Exception as e:  # pylint: disable=W0718
            return f"unknown ({type(e).__name__})"
    indexdir = os.path.join(args.root, "indexes", args.cell)
    embeddings.save(indexdir)
    disk_kb = int(sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(indexdir) for f in fs) / 1024)

    start = time.time()
    results, offset = {}, 0
    for b in range(0, len(queries), 256):
        batch = queries[b : b + 256]
        for i, r in enumerate(embeddings.batchsearch(batch, args.limit + 1)):
            r = [(x["id"], x["score"]) for x in r] if r and isinstance(r[0], dict) else list(r)
            r = [(uid, score) for uid, score in r if uid != uids[offset + i]][: args.limit]
            results[uids[offset + i]] = dict(r)
        offset += len(batch)
    searchtime = round(time.time() - start, 2)
    index_desc = describe_index()
    nprobe_used = getattr(ann.backend, "nprobe", None)
    nprobe_used = int(nprobe_used) if isinstance(nprobe_used, (int, float)) else None
    try:
        nprobe_config = int(ann.nprobe())
    except Exception:  # pylint: disable=W0718
        nprobe_config = None
    evaluator = pytrec_eval.RelevanceEvaluator(qrels, MEASURES)
    perq = evaluator.evaluate(results)
    rows = []
    for qid in uids:
        m = perq.get(qid, {})
        rows.append({"qid": qid, "nresults": len(results.get(qid, {})), **{k: float(m.get(k, 0.0)) for k in METRIC_KEYS}})
    write_jsonl(os.path.join(args.root, "perquery", f"{args.cell}.jsonl"), rows)
    metrics = {k: round(float(np.mean([r[k] for r in rows])), 5) for k in METRIC_KEYS}
    cell = {
        "cell": args.cell,
        "corpus": args.corpus,
        "artifact": args.artifact,
        "encoder": encoder_desc,
        "variant": args.variant,
        "ann": args.ann,
        "ann_effective": "exact" if (args.ann == "exact" or len(ids) <= IVF_THRESHOLD) else "default-ivf",
        "faiss_components": components,
        "faiss_index": index_desc,
        "nprobe_used": nprobe_used,
        "nprobe_config": nprobe_config,
        "n_docs": len(ids),
        "n_queries_scored": len(uids),
        "queries_under_limit": sum(1 for r in rows if r["nresults"] < args.limit),
        "queries_zero_results": sum(1 for r in rows if r["nresults"] == 0),
        "resolved_center": center_info,
        "encoder_class": type(encoder).__name__ if encoder is not None else None,
        "encoder_has_center": bool(getattr(encoder, "center", None) is not None) if encoder is not None else None,
        "pooling_class": type(pooling).__name__,
        "index_seconds": indextime,
        "search_seconds": searchtime,
        "disk_kb": disk_kb,
        "metrics": metrics,
        "cuda": cuda_stats(),
        "time": now(),
    }
    write_json(cellpath, cell)
    print(json.dumps({k: cell[k] for k in ["cell", "ann_effective", "faiss_components", "faiss_index", "resolved_center", "metrics", "index_seconds", "search_seconds", "queries_under_limit"]}))


# ----------------------------------------------------------------------------- summarize


def load_cells(root):
    cells = {}
    cdir = os.path.join(root, "cells")
    if not os.path.isdir(cdir):
        return cells
    for f in sorted(os.listdir(cdir)):
        if f.endswith(".json"):
            try:
                c = read_json(os.path.join(cdir, f))
                cells[c["cell"]] = c
            except Exception as e:  # pylint: disable=W0718
                print("skipping corrupt cell", f, e)
    return cells


def perquery_map(root, cell):
    path = os.path.join(root, "perquery", f"{cell}.jsonl")
    if not os.path.exists(path):
        return None
    return {r["qid"]: r["ndcg_cut_10"] for r in read_jsonl(path)}


def bootstrap_ratio(delta, tc, n=10000, seed=20260823):
    """Query bootstrap of mean(delta)/mean(tc); returns point estimate + one-sided 95% upper bound."""
    import numpy as np

    rng = np.random.default_rng(seed)
    delta, tc = np.asarray(delta), np.asarray(tc)
    m = len(delta)
    ratios, dm, tm = [], [], []
    for _ in range(n):
        idx = rng.integers(0, m, m)
        d, t = delta[idx].mean(), tc[idx].mean()
        dm.append(d)
        tm.append(t)
        ratios.append(d / t if t > 0 else np.inf)
    ratios = np.asarray(ratios)
    return {"delta_c": float(delta.mean()), "T_c": float(tc.mean()), "ratio": float(delta.mean() / tc.mean()) if tc.mean() > 0 else None, "ratio_upper95_onesided": float(np.percentile(ratios[np.isfinite(ratios)], 95)) if np.isfinite(ratios).any() else None, "T_c_lower95": float(np.percentile(tm, 5)), "delta_c_ci90": [float(np.percentile(dm, 5)), float(np.percentile(dm, 95))], "frac_T_c_nonpositive": float((np.asarray(tm) <= 0).mean())}


def bootstrap_lower(values, n=10000, seed=20260823):
    import numpy as np

    rng = np.random.default_rng(seed)
    v = np.asarray(values)
    means = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(n)]
    return {"mean": float(v.mean()), "lower95_onesided": float(np.percentile(means, 5))}


def cmd_summarize(args):
    import numpy as np

    cells = load_cells(args.root)
    seeds = [int(s) for s in args.seeds.split(",")]
    corpora = args.corpora.split(",")
    lines = ["# RESULTS — LEMUR portability pilot, ColBERTv2", ""]
    env = read_json(os.path.join(args.root, "env.json"), required=False) or {}
    lines.append(f"env: txtai_head={env.get('txtai_head', '?')} pin_ok={env.get('txtai_head_matches_pin')} torch={env.get('torch')} device=consumer-gpu colbert_rev={COLBERT_REV} lighton_rev={LIGHTON_REV} generated={now()}")
    lines.append(f"cells completed: {len(cells)}")
    lines.append("")
    lines.append("## STATUS: " + ("PARTIAL" if args.partial else "COMPLETE"))
    lines.append("")
    summary = {"generated": now(), "cells": len(cells), "per_corpus": {}}

    def cellname(corpus, arm, seed, ann):
        return f"{corpus}--{arm}--s{seed}--{ann}"

    arms_headline = ["percorpus-mlp", "percorpus-elm", "portable-mlp", "portable-elm"]
    arms_extra = ["portable-mlp-remean", "portable-elm-remean", "portable-mlp-recal", "portable-elm-recal", "portable-mlp-basis"]
    for corpus in corpora:
        legs = ["exact"] if any(c["corpus"] == corpus and c["n_docs"] <= IVF_THRESHOLD for c in cells.values()) else ["exact", "default"]
        summary["per_corpus"][corpus] = {}
        lines.append(f"## {corpus}")
        lines.append("")
        for ann in legs:
            lines.append(f"### ANN leg: {ann}")
            lines.append("")
            lines.append("| arm | " + " | ".join(f"seed {s}" for s in seeds) + " | mean nDCG@10 |")
            lines.append("|---|" + "---:|" * (len(seeds) + 1))
            armmeans = {}
            for arm in arms_headline + arms_extra:
                vals = []
                for s in seeds:
                    c = cells.get(cellname(corpus, arm, s, ann))
                    vals.append(c["metrics"]["ndcg_cut_10"] if c else None)
                present = [v for v in vals if v is not None]
                armmeans[arm] = float(np.mean(present)) if present else None
                if present:
                    lines.append(f"| {arm} | " + " | ".join(f"{v:.5f}" if v is not None else "—" for v in vals) + f" | {armmeans[arm]:.5f} |")
            for m in ("muvera-20,5,16", "muvera-4,5,16", "muvera-20,2,32"):
                c = cells.get(f"{corpus}--{m}--{ann}")
                if c:
                    lines.append(f"| {m} ({c['encoder']}) | " + " | ".join("—" for _ in seeds) + f" | {c['metrics']['ndcg_cut_10']:.5f} |")
                    armmeans[m] = c["metrics"]["ndcg_cut_10"]
            lines.append("")
            # paired per-query statistics (seed-averaged per query, then bootstrap over queries)
            stats = {}

            def seedavg(arm):
                maps = [perquery_map(args.root, cellname(corpus, arm, s, ann)) for s in seeds]
                maps = [m for m in maps if m]
                if not maps:
                    return None
                qids = set.intersection(*[set(m) for m in maps])
                return {q: float(np.mean([m[q] for m in maps])) for q in qids}

            pm, pe, tm, te = seedavg("portable-mlp"), seedavg("portable-elm"), seedavg("percorpus-mlp"), seedavg("percorpus-elm")
            if pm and tm and te:
                qids = sorted(set(pm) & set(tm) & set(te))
                delta = [tm[q] - pm[q] for q in qids]
                tc = [tm[q] - te[q] for q in qids]
                stats["portability"] = {"n_queries": len(qids), **bootstrap_ratio(delta, tc)}
            if pm and pe:
                qids = sorted(set(pm) & set(pe))
                stats["portable_mlp_minus_portable_elm"] = bootstrap_lower([pm[q] - pe[q] for q in qids])
            mv = perquery_map(args.root, f"{corpus}--muvera-20,5,16--{ann}")
            if pm and mv:
                qids = sorted(set(pm) & set(mv))
                stats["portable_mlp_minus_muvera10240"] = bootstrap_lower([pm[q] - mv[q] for q in qids])
            for arm in ("portable-mlp", "portable-elm"):
                base, rem, rec = armmeans.get(arm), armmeans.get(f"{arm}-remean"), armmeans.get(f"{arm}-recal")
                ref = armmeans.get(arm.replace("portable", "percorpus"))
                if base is not None and ref is not None:
                    penalty = ref - base
                    stats[f"{arm}_penalty_decomposition"] = {"total_penalty": penalty, "remean_recovery": (rem - base) if rem is not None else None, "recal_recovery": (rec - base) if rec is not None else None, "residual": (penalty - ((rem - base) if rem is not None else 0) - ((rec - base) if rec is not None else 0))}
            summary["per_corpus"][corpus][ann] = {"arm_means": armmeans, "stats": stats}
            if stats:
                lines.append("```")
                lines.append(json.dumps(stats, indent=2, sort_keys=True))
                lines.append("```")
                lines.append("")
    # legacy replication control
    legacy = cells.get("nfcorpus--legacy-mlp-center-false--s42--exact")
    lines.append("## Out-of-matrix legacy replication control (nfcorpus / MLP / seed 42 / center:false both ends)")
    if legacy:
        v = legacy["metrics"]["ndcg_cut_10"]
        lines.append(f"nDCG@10 = {v:.5f} vs previously recorded 0.25524 (diff {v - 0.25524:+.5f}; the prior control table drifted 0.25534 vs 0.25524, so a tolerance of ±0.002 is the reading aid, not a gate)")
        summary["legacy_control"] = {"ndcg_cut_10": v, "banked": 0.25524, "diff": v - 0.25524}
    else:
        lines.append("not run")
    lines.append("")
    # preflight
    pdir = os.path.join(args.root, "preflight")
    if os.path.isdir(pdir):
        lines.append("## Preflight — calibration z = (maxsim(docs, sample) - mean) / std on target docs")
        lines.append("")
        lines.append("| artifact | corpus | docs | mean z | sd z | p5 | p50 | p95 | frac<0 | frac<-2 |")
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        summary["preflight"] = {}
        for f in sorted(os.listdir(pdir)):
            p = read_json(os.path.join(pdir, f))
            lines.append(f"| {p['artifact']} | {p['corpus']} | {p['n_docs']} | {p['mean']:.4f} | {p['sd']:.4f} | {p['p5']:.3f} | {p['p50']:.3f} | {p['p95']:.3f} | {p['frac_below_zero']:.4f} | {p['frac_below_minus2']:.4f} |")
            summary["preflight"][f] = p
        lines.append("")
    # artifacts
    adir = os.path.join(args.root, "artifacts")
    if os.path.isdir(adir):
        lines.append("## Artifacts")
        lines.append("")
        lines.append("| artifact | data | n | type | seed | epoch/loss | wall s | peak VRAM GB | center key | sample rank | cond |")
        lines.append("|---|---|---:|---|---:|---|---:|---:|---|---:|---:|")
        summary["artifacts"] = {}
        for a in sorted(os.listdir(adir)):
            t = os.path.join(adir, a, "train.json")
            if os.path.exists(t):
                r = read_json(t)
                ar = r["artifact_report"]
                lines.append(f"| {a} | {r['data']} | {r['n_texts']} | {r['modeltype']} | {r['seed']} | {r.get('selectedepoch')}/{(r.get('selectedloss') or 0):.5f} | {r['wall_seconds']} | {r['cuda'].get('max_allocated_gb', '—')} | {'yes' if ar.get('center_sha256') else 'no'} | {ar['sample_rank_at_tolerance']} | {ar['sample_condition_number']:.1f} |")
                summary["artifacts"][a] = {k: r[k] for k in ["data", "n_texts", "modeltype", "seed", "wall_seconds", "cuda", "selectedepoch", "selectedloss"]}
        lines.append("")
    # every cell row
    lines.append("## All cells")
    lines.append("")
    lines.append("| cell | ann (effective) | components | nDCG@10 | MAP@10 | R@10 | P@10 | q<10 | center | index s | search s |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|")
    for name, c in sorted(cells.items()):
        m = c["metrics"]
        rc = c.get("resolved_center")
        rcs = f"{rc['scope']}:{rc.get('mean_sha256', '')[:8]}" if rc else "none"
        fidx = c.get("faiss_index") or "?"
        if c.get("nprobe_used") is None and "nlist=" in fidx and "nprobe=1)" in fidx:
            # descriptor captured before search by an earlier harness revision; txtai searched at round(nlist/16)
            import re

            nlist = int(re.search(r"nlist=(\d+)", fidx).group(1))
            fidx = fidx.replace("nprobe=1)", f"nprobe={round(nlist / 16)}†)")
        lines.append(f"| {name} | {c['ann']} ({c['ann_effective']}) | {c.get('faiss_components') or 'auto'} → {fidx} | {m['ndcg_cut_10']:.5f} | {m['map_cut_10']:.5f} | {m['recall_10']:.5f} | {m['P_10']:.5f} | {c['queries_under_limit']} | {rcs} | {c['index_seconds']} | {c['search_seconds']} |")
    lines.append("")
    lines.append("## Honest notes")
    lines.append("")
    lines.append("Development-pilot numbers over development corpora; not a shipping benchmark.")
    lines.append("")
    lines.append("† nprobe shown as txtai's search-time rule round(nlist/16): these cells were recorded by harness revision 1, whose index descriptor was captured before search (faiss default nprobe=1 in the string); the searches themselves ran at txtai's value. Later cells record `nprobe_used` directly.")
    out = os.path.join(args.root, "RESULTS.md")
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=args.root)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, out)
    write_json(os.path.join(args.root, "summary.json"), summary)
    print("\n".join(lines[:12]))


# ----------------------------------------------------------------------------- cli


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", default=".")
    p.add_argument("--cpu", action="store_true", help="force CPU (smoke tests)")
    p.add_argument("--model-path", default=None, help="local ColBERT model dir (overrides the pinned colbertv2 snapshot)")
    p.add_argument("--allow-download", action="store_true", help="let snapshot_download fetch the colbert model if absent")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("env")
    s.add_argument("--checkout", default=None, help="pinned txtai checkout dir to assert against")
    s.set_defaults(fn=cmd_env)

    s = sub.add_parser("prep-targets")
    s.add_argument("--beir", required=True)
    s.add_argument("--corpora", default="nfcorpus,scifact,arguana")
    s.add_argument("--mini", type=int, default=0, help="smoke: keep only the first N docs and matching qrels")
    s.set_defaults(fn=cmd_prep_targets)

    s = sub.add_parser("prep-source")
    s.add_argument("--name", required=True)
    s.add_argument("--total", type=int, required=True)
    s.add_argument("--seed", type=int, required=True)
    s.add_argument("--constituents", default=",".join(CONSTITUENTS))
    s.add_argument("--hf-dir", default=None, help="already-downloaded dataset dir (skips snapshot_download)")
    s.add_argument("--from-beir", default=None, help="smoke only: draw from a staged BEIR corpus instead of the mixture")
    s.set_defaults(fn=cmd_prep_source)

    s = sub.add_parser("train")
    s.add_argument("--artifact", required=True)
    s.add_argument("--data", required=True, help="target:<corpus> | source:<draw>")
    s.add_argument("--modeltype", choices=["mlp", "elm"], required=True)
    s.add_argument("--seed", type=int, required=True)
    s.add_argument("--corpussubsetsize", type=int, default=None)
    s.add_argument("--center-false", action="store_true", help="legacy regime: explicit center False at training")
    s.set_defaults(fn=cmd_train)

    s = sub.add_parser("remean")
    s.add_argument("--corpus", required=True)
    s.set_defaults(fn=cmd_remean)

    s = sub.add_parser("recal")
    s.add_argument("--artifact", required=True)
    s.add_argument("--corpus", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--n", type=int, default=8192)
    s.add_argument("--seed", type=int, default=20260823)
    s.set_defaults(fn=cmd_recal)

    s = sub.add_parser("preflight")
    s.add_argument("--artifact", required=True)
    s.add_argument("--corpus", required=True)
    s.add_argument("--n", type=int, default=2000)
    s.add_argument("--seed", type=int, default=20260823)
    s.set_defaults(fn=cmd_preflight)

    s = sub.add_parser("index-eval")
    s.add_argument("--cell", required=True)
    s.add_argument("--corpus", required=True)
    s.add_argument("--artifact", required=True, help="<artifact dir name> | muvera:<reps>,<hashes>,<proj>")
    s.add_argument("--ann", choices=["exact", "default"], required=True)
    s.add_argument("--variant", choices=["default", "remean", "legacy"], default="default")
    s.add_argument("--limit", type=int, default=10)
    s.set_defaults(fn=cmd_index_eval)

    s = sub.add_parser("summarize")
    s.add_argument("--seeds", default="1,2,3")
    s.add_argument("--corpora", default="nfcorpus,scifact,arguana")
    s.add_argument("--partial", action="store_true")
    s.set_defaults(fn=cmd_summarize)

    args = p.parse_args()
    args.root = os.path.abspath(args.root)
    os.makedirs(args.root, exist_ok=True)
    args.fn(args)


if __name__ == "__main__":
    main()
