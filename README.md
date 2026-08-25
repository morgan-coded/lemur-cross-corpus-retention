# One frozen LEMUR artifact does not transfer for ColBERTv2

One general LEMUR artifact trained on a frozen source-mixture draw does not preserve the per-corpus training gain. Under exact search it retains about 43% of that gain at best on nfcorpus and arguana, retains none on scifact, and is a statistical tie with the single-encode MUVERA-10240 reference on all three corpora; on the measured default-IVF legs it trails it. The negative result is the result: for this encoder and recipe, per-corpus training remains the supported choice.

## The question

The maintainer's question in [txtai PR 1068](https://github.com/neuml/txtai/pull/1068#discussion_r3006653791) was whether one general LEMUR model could generalize across datasets rather than stay dataset-specific. [Issue 1173](https://github.com/neuml/txtai/issues/1173) turned that into a default-model question. The [LEMUR paper](https://arxiv.org/abs/2601.21853) leaves synthetic and cross-corpus training sets as future work. This pilot tests the narrow first case: one encoder, one declared cross-corpus mixture, then three held-out development corpora.

The comparison uses the implementation and baseline conventions described in the [NeuML LEMUR article](https://huggingface.co/blog/NeuML/txtai-lemur). It asks about transfer, not whether LEMUR works when trained on the target corpus. The per-corpus arm clears MUVERA-10240 on every exact-search leg at one-fifth the width; what fails is transfer.

## Design

The matrix crosses four conditions: target-corpus versus frozen-source training, and trained MLP (`epochs=100`) versus no-epoch ELM (`epochs=0`). Each condition uses seeds 1, 2, and 3 with ColBERTv2 pinned at `c1e84128`. Every LEMUR artifact projects to 2,048 dimensions. The targets contain 3,633 nfcorpus documents, 5,183 scifact documents, and 8,674 arguana documents.

The portable arm trains on one 8,192-document equal-stratified draw from the pinned LightOn mixture. Fever and fiqa contribute 1,171 documents each; hotpotqa, msmarco, nq, squadv2, and trivia contribute 1,170 each. Seed 20260823 and the selected document identifiers are frozen in `results/draw8192.manifest.json`. A separate 3,101-document draw at seed 20260824 supports the basis-matched probe.

Every corpus has an exact `IDMap,Flat` leg. Scifact and arguana also have txtai-default IVF legs because they cross the 5,000-row switch. Evaluation uses nDCG@10 from `pytrec_eval`, with per-query values retained. The single-encode MUVERA controls are 10,240 dimensions `(20,5,16)`, 2,048 dimensions `(4,5,16)`, and 2,560 dimensions `(20,2,32)`.

## Results

Exact-search seed means put the transfer loss in the open:

| corpus | per-corpus MLP | portable MLP | MUVERA-10240 | retained per-corpus gain |
|---|---:|---:|---:|---:|
| nfcorpus | 0.27607 | 0.23987 | 0.24015 | 39.27% |
| scifact | 0.54415 | 0.46598 | 0.48130 | -55.62% |
| arguana | 0.40487 | 0.35005 | 0.34758 | 43.07% |

MUVERA rows are single encodes at the shipped configurations; seed columns do not apply.

Retention is `(portable MLP - per-corpus ELM) / (per-corpus MLP - per-corpus ELM)`. The zero point is the per-corpus ELM: at a matched seed its feature map is identical across arms, so it prices the no-epoch floor on the target. A negative value means the portable MLP falls below the per-corpus ELM control. Scifact does exactly that. The `delta/T` ratio below equals `1 - retention`; both share the denominator `T`, and derived values are computed at full precision before rounding. Nfcorpus is level with MUVERA-10240. Neither remaining exact-search gap separates from a tie by the paired bounds: arguana's 0.00247 advantage carries a lower bound of -0.00701, and scifact's 0.01532 deficit an upper bound near +0.006. Under exact search the comparison is three statistical ties; the retention and loss tables carry the transfer verdict.

The separate default-IVF legs are also negative against full-width MUVERA:

| corpus | per-corpus MLP | portable MLP | MUVERA-10240 | retained per-corpus gain |
|---|---:|---:|---:|---:|
| scifact | 0.38008 | 0.31485 | 0.35957 | -30.68% |
| arguana | 0.40107 | 0.31480 | 0.34256 | 26.05% |

For the loss analysis, `delta` is per-corpus MLP minus portable MLP and `T` is per-corpus MLP minus per-corpus ELM. The ratio `delta/T` is the lost fraction of the per-corpus gain. Its reported uncertainty is the one-sided 95% upper bound from 10,000 paired query-bootstrap resamples.

| search path | delta | T | delta/T | one-sided 95% upper |
|---|---:|---:|---:|---:|
| nfcorpus exact | 0.03619 | 0.05960 | 0.607 | 0.771 |
| scifact exact | 0.07817 | 0.05023 | 1.556 | 2.018 |
| arguana exact | 0.05482 | 0.09630 | 0.569 | 0.644 |
| scifact default IVF | 0.06523 | 0.04992 | 1.307 | 2.237 |
| arguana default IVF | 0.08627 | 0.11667 | 0.739 | 0.818 |

Three probes narrow the failure. Rewriting only the target calibration mean and standard deviation moves the five portable means by -0.00740 to +0.00026; roughly 0.007 at the largest cell does not rescue transfer. Substituting the target token mean hurts nfcorpus and scifact, while improving arguana, so centering is not a general repair. Training on the 3,101-document basis-matched draw stays within 0.0052 of the main portable result in every leg; the loss is not a source-basis-size artifact.

Width is still useful. Under exact search, portable LEMUR-2048 clears the single-encode MUVERA-2048 control by 0.07578, 0.11348, and 0.09089: about 0.08-0.11 across all three corpora. That does not answer the general-artifact question because the shipped MUVERA reference is 10,240 dimensions. The out-of-matrix nfcorpus legacy control reproduces the previously recorded 0.25524 exactly.

## ANN results, corpus by corpus

Nfcorpus has 3,633 rows, so txtai's default is exact below the 5,000-row IVF switch. There is no nfcorpus IVF result in this pilot.

Scifact and arguana each have one default-IVF index partition per cell. A separate public scifact partition grid measured roughly 0.01-0.02 nDCG@10 of single-partition spread per arm; the details are in the [Hugging Face thread](https://huggingface.co/posts/davidmezzetti/477658488813407). Arguana's default index runs 222 cells at about the same 39 documents per centroid, so that scale is assumed there, not measured. A deficit differences two independent partitions, so its reading scale is about 0.026 at the measured worst case. Scifact's 0.04472 deficit against MUVERA-10240 clears it; that negative sign is called. Arguana's 0.02776 does not clear it and is reported without a sign call. Smaller ANN differences should not be read as stable from one partition.

## Reproduction

The harness is `harness/pilot.py`; the ordered guide is in `harness/REPRO.md`. The immutable pins are txtai `20f818f7`, ColBERTv2 `c1e84128`, and `lightonai/embeddings-fine-tuning` `1ca46333`. Model seeds are 1, 2, and 3. The source-draw seeds are 20260823 and 20260824, with both manifests published beside the results.

The source dataset card declares no license. The reproduction path fetches only pinned `documents/*.parquet` files by script from upstream. This repository does not contain the mixture, mined scores, queries, or trained artifacts. It publishes scripts, pins, manifests, aggregate cells, and per-query measurements. The completed run used one consumer GPU; the path-free dependency record is `results/reproduction-environment.json`.

The published per-query rows recompute every paired summary in this write-up without re-running retrieval; they do not reconstruct the excluded encodings or source text.

## Scope and non-claims

This is a development pilot over one encoder, one equal-stratified mixture recipe, one main draw size, and three development corpora. It is evidence against this portable recipe, not a claim that cross-corpus LEMUR training can never work. Other encoders, mixture compositions, objectives, and larger source scales could change the answer. Testing those is future work, not a commitment attached to this result.

## License

MIT. The pinned upstream datasets and models keep their own terms; the source mixture is not redistributed here.
