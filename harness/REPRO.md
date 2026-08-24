# Reproducing the pilot

This guide reconstructs the run layout consumed by `pilot.py`. It publishes commands and immutable pins, not trained artifacts or source-mixture data.

## Pins and environment

- txtai: `20f818f72cacbdc7ea01912788a4b988db029c5e`
- `colbert-ir/colbertv2.0`: `c1e84128e85ef755c096a95bdb06b47793b13acf`
- `lightonai/embeddings-fine-tuning`: `1ca463331ed637d25c1058567e932e0d3bad2983`
- Python 3.14.5, torch 2.13.0+cu130, Faiss 1.14.3, NumPy 2.5.1, pytrec_eval 0.5.10
- Also imported: `transformers`, `huggingface_hub`, `pyarrow`, `safetensors` (versions not pinned by the run record; use releases compatible with the torch pin)
- One consumer GPU was used for the recorded run. `--cpu` is available for smoke tests.

The source dataset card declares no license. `prep-source` fetches only `documents/*.parquet` at the pinned revision. Do not redistribute the mixture, its mined scores, its queries, or trained derivatives. The published manifests contain identifiers, counts, revision pins, and duplicate-audit results without re-hosting source text.

## Inputs

Prepare a txtai checkout at the pinned commit, a local ColBERTv2 snapshot at the pinned revision, and BEIR-format copies of nfcorpus, scifact, and arguana. Each target needs `corpus.jsonl`, `queries.jsonl`, and `qrels/test.tsv`. The corpora come from the public [BEIR benchmark](https://github.com/beir-cellar/beir) dataset archives, which unzip to exactly that layout. The ColBERTv2 snapshot can be fetched by the harness itself with `--allow-download`, which downloads only the pinned revision.

Set path variables without embedding them in result files:

```bash
TXTAI_CHECKOUT=/path/to/txtai
MODEL_DIR=/path/to/colbertv2-snapshot
BEIR_DIR=/path/to/beir
RUN_DIR=/path/to/lemur-pilot-run
export PYTHONPATH="$TXTAI_CHECKOUT/src/python"
mkdir -p "$RUN_DIR"
```

All global harness options precede the subcommand.

## Prepare and verify

```bash
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" env --checkout "$TXTAI_CHECKOUT"
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" prep-targets --beir "$BEIR_DIR" --corpora nfcorpus,scifact,arguana
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" prep-source --name draw8192 --total 8192 --seed 20260823
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" prep-source --name draw3101 --total 3101 --seed 20260824

for corpus in nfcorpus scifact arguana; do
  python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" remean --corpus "$corpus"
done
```

The two generated manifests must match `results/draw8192.manifest.json` and `results/draw3101.manifest.json`, including `ids_sha256`. If they do not, stop before training.

## Train the four conditions

```bash
for seed in 1 2 3; do
  python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" train --artifact "portable-mlp-s$seed" --data source:draw8192 --modeltype mlp --seed "$seed"
  python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" train --artifact "portable-elm-s$seed" --data source:draw8192 --modeltype elm --seed "$seed"
  python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" train --artifact "portable-mlp-basis-s$seed" --data source:draw3101 --modeltype mlp --seed "$seed"

  for corpus in nfcorpus scifact arguana; do
    python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" train --artifact "$corpus-mlp-s$seed" --data "target:$corpus" --modeltype mlp --seed "$seed"
    python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" train --artifact "$corpus-elm-s$seed" --data "target:$corpus" --modeltype elm --seed "$seed"
    python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" recal --artifact "portable-mlp-s$seed" --corpus "$corpus" --out "portable-mlp-s$seed-recal-$corpus" --seed 20260823
    python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" recal --artifact "portable-elm-s$seed" --corpus "$corpus" --out "portable-elm-s$seed-recal-$corpus" --seed 20260823
  done
done
```

MLP uses 100 epochs and a 0.1 validation split. ELM uses zero epochs and no validation split. The fixed fit parameters are declared near the top of `pilot.py`; the trainer's 8,192-document default remains unmodified.

## Evaluate

`index-eval` writes one atomic cell JSON plus one per-query JSONL file. Exact search uses `--ann exact`; only scifact and arguana receive a separate `--ann default` leg. The staged filenames under `results/cells/` are the complete expected cell inventory and each file records its artifact, variant, ANN mode, and encoder description.

Examples covering the main variants and a baseline:

```bash
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" index-eval --cell nfcorpus--portable-mlp--s1--exact --corpus nfcorpus --artifact portable-mlp-s1 --ann exact
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" index-eval --cell scifact--portable-mlp-remean--s1--default --corpus scifact --artifact portable-mlp-s1 --ann default --variant remean
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" index-eval --cell arguana--portable-mlp-recal--s1--exact --corpus arguana --artifact portable-mlp-s1-recal-arguana --ann exact
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" index-eval --cell scifact--muvera-20,5,16--exact --corpus scifact --artifact muvera:20,5,16 --ann exact
```

Run `preflight` for seed-1 portable, basis-matched, and matching per-corpus artifacts on their target corpora. The expected 15 outputs are listed under `results/preflight/`.

The legacy control is separate from the four-condition matrix:

```bash
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" train --artifact legacy-nfcorpus-mlp-s42 --data target:nfcorpus --modeltype mlp --seed 42 --center-false
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" index-eval --cell nfcorpus--legacy-mlp-center-false--s42--exact --corpus nfcorpus --artifact legacy-nfcorpus-mlp-s42 --ann exact --variant legacy
```

After every staged cell exists:

```bash
python harness/pilot.py --root "$RUN_DIR" --model-path "$MODEL_DIR" summarize --seeds 1,2,3 --corpora nfcorpus,scifact,arguana
```

Compare the generated `RESULTS.md`, `summary.json`, `stats.json`, cell JSON, per-query JSONL, and preflight JSON against the published copies. `results/units.log` is the 223-unit completion inventory from the recorded run.
