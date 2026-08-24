# Context and design evidence

This path-free note keeps the write-up's non-result claims auditable beside the measured files.

## Question and prior record

- In [txtai PR 1068](https://github.com/neuml/txtai/pull/1068#discussion_r3006653791), the maintainer asked whether one general LEMUR model could generalize to other datasets instead of remaining dataset-specific.
- [txtai issue 1173](https://github.com/neuml/txtai/issues/1173) carried that question into a proposed default-model design and the completed development pilot summarized here.
- The [LEMUR paper](https://arxiv.org/abs/2601.21853) says: "we leave the investigation of synthetic and cross-corpus training sets as future work."
- The shipped txtai baseline and earlier exact-search measurements are described in the [NeuML LEMUR article](https://huggingface.co/blog/NeuML/txtai-lemur).

## Frozen pilot design

- Encoder: `colbert-ir/colbertv2.0` at revision `c1e84128e85ef755c096a95bdb06b47793b13acf`.
- txtai: revision `20f818f72cacbdc7ea01912788a4b988db029c5e`.
- Conditions: target-trained and frozen-source, crossed with trained MLP (`epochs=100`) and untrained ELM (`epochs=0`), at seeds 1, 2, and 3.
- Targets: nfcorpus, scifact, and arguana. Their document counts and effective default index types are in `stats.json`.
- Source: an equal-stratified document draw from `lightonai/embeddings-fine-tuning` at revision `1ca463331ed637d25c1058567e932e0d3bad2983`; constituents were fever, fiqa, hotpotqa, msmarco, nq, squadv2, and trivia.
- The main draw used 8,192 documents at seed 20260823. The basis-matched draw used 3,101 documents at seed 20260824. Both selections and constituent counts are frozen in their manifests.
- Search: exact `IDMap,Flat` for every corpus; the txtai default path additionally measured on scifact and arguana, which are above the 5,000-row IVF switch. Below that switch, nfcorpus's default path is exact.
- Metric: nDCG at 10 from `pytrec_eval`, with per-query scores retained for paired inference.
- Single-encode MUVERA controls: 10,240 dimensions from `(20,5,16)`, 2,048 from `(4,5,16)`, and 2,560 from `(20,2,32)`.
- Inference: `delta` is per-corpus MLP minus portable MLP; `T` is per-corpus MLP minus per-corpus ELM. The ratio `delta/T` used 10,000 paired query-bootstrap resamples and a one-sided 95% upper bound.

## Publication boundary

The source dataset card declares no license. Reproduction may fetch the pinned `documents/*.parquet` files by script from upstream, but this repository does not re-host the mixture, queries, mined scores, trained artifacts, or other mixture derivatives. An official reusable artifact would require license clarification or reconstruction from explicitly compatible constituent sources.

The completed run used one consumer GPU. Exact dependency versions and full immutable pins are in `reproduction-environment.json`; the command sequence is in `../harness/REPRO.md`.

## ANN caveat evidence

A separate public scifact/ColBERTv2 IVF132 partition grid measured 40 alternate partitions. Across the reported probe grid, LEMUR nDCG-at-10 standard deviations ranged from 0.01022 to 0.01892; the comparable MUVERA range was 0.00345 to 0.01803. That supports using roughly 0.01-0.02 nDCG at 10 as a reading scale for a single partition, not as an interval for the retention experiment. The source conversation is the [public Hugging Face thread](https://huggingface.co/posts/davidmezzetti/477658488813407); the extracted values are in `partition-variance.json`.
