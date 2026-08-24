# RESULTS — LEMUR portability pilot, ColBERTv2

env: txtai_head=20f818f72cacbdc7ea01912788a4b988db029c5e pin_ok=True torch=2.13.0+cu130 device=consumer-gpu colbert_rev=c1e84128e85ef755c096a95bdb06b47793b13acf lighton_rev=1ca463331ed637d25c1058567e932e0d3bad2983 generated=2026-08-23T05:07:28Z
cells completed: 151

## STATUS: COMPLETE

## nfcorpus

### ANN leg: exact

| arm | seed 1 | seed 2 | seed 3 | mean nDCG@10 |
|---|---:|---:|---:|---:|
| percorpus-mlp | 0.27346 | 0.27865 | 0.27609 | 0.27607 |
| percorpus-elm | 0.21094 | 0.21617 | 0.22230 | 0.21647 |
| portable-mlp | 0.24143 | 0.24133 | 0.23686 | 0.23987 |
| portable-elm | 0.20825 | 0.21349 | 0.20317 | 0.20830 |
| portable-mlp-remean | 0.21479 | 0.21214 | 0.20776 | 0.21156 |
| portable-elm-remean | 0.16969 | 0.17753 | 0.16775 | 0.17166 |
| portable-mlp-recal | 0.24143 | 0.24145 | 0.23688 | 0.23992 |
| portable-elm-recal | 0.20821 | 0.21298 | 0.20305 | 0.20808 |
| portable-mlp-basis | 0.23650 | 0.23553 | 0.23369 | 0.23524 |
| muvera-20,5,16 (muvera r20 h5 p16 = 10240 dims) | — | — | — | 0.24015 |
| muvera-4,5,16 (muvera r4 h5 p16 = 2048 dims) | — | — | — | 0.16409 |
| muvera-20,2,32 (muvera r20 h2 p32 = 2560 dims) | — | — | — | 0.18455 |

```
{
  "portability": {
    "T_c": 0.05959909021118905,
    "T_c_lower95": 0.04834683427480467,
    "delta_c": 0.03619175791895922,
    "delta_c_ci90": [
      0.02617865699845155,
      0.045764892846469285
    ],
    "frac_T_c_nonpositive": 0.0,
    "n_queries": 323,
    "ratio": 0.6072535300574878,
    "ratio_upper95_onesided": 0.7713977991709721
  },
  "portable-elm_penalty_decomposition": {
    "recal_recovery": -0.00022333333333329763,
    "remean_recovery": -0.03664666666666666,
    "residual": 0.04503666666666667,
    "total_penalty": 0.008166666666666711
  },
  "portable-mlp_penalty_decomposition": {
    "recal_recovery": 4.6666666666694834e-05,
    "remean_recovery": -0.028309999999999974,
    "residual": 0.06445666666666666,
    "total_penalty": 0.03619333333333338
  },
  "portable_mlp_minus_muvera10240": {
    "lower95_onesided": -0.00992626758304322,
    "mean": -0.0002759905904644195
  },
  "portable_mlp_minus_portable_elm": {
    "lower95_onesided": 0.023146795553124787,
    "mean": 0.03157479674631855
  }
}
```

## scifact

### ANN leg: exact

| arm | seed 1 | seed 2 | seed 3 | mean nDCG@10 |
|---|---:|---:|---:|---:|
| percorpus-mlp | 0.54805 | 0.54687 | 0.53753 | 0.54415 |
| percorpus-elm | 0.50513 | 0.47955 | 0.49708 | 0.49392 |
| portable-mlp | 0.46689 | 0.46177 | 0.46929 | 0.46598 |
| portable-elm | 0.37682 | 0.39061 | 0.37640 | 0.38128 |
| portable-mlp-remean | 0.44461 | 0.44834 | 0.45618 | 0.44971 |
| portable-elm-remean | 0.35377 | 0.36930 | 0.34528 | 0.35612 |
| portable-mlp-recal | 0.46693 | 0.46220 | 0.46960 | 0.46624 |
| portable-elm-recal | 0.37864 | 0.39366 | 0.37673 | 0.38301 |
| portable-mlp-basis | 0.47633 | 0.46744 | 0.45175 | 0.46517 |
| muvera-20,5,16 (muvera r20 h5 p16 = 10240 dims) | — | — | — | 0.48130 |
| muvera-4,5,16 (muvera r4 h5 p16 = 2048 dims) | — | — | — | 0.35250 |
| muvera-20,2,32 (muvera r20 h2 p32 = 2560 dims) | — | — | — | 0.36595 |

```
{
  "portability": {
    "T_c": 0.050226222685192154,
    "T_c_lower95": 0.036867170220859787,
    "delta_c": 0.07816821290375292,
    "delta_c_ci90": [
      0.057891873802500424,
      0.09981174114234402
    ],
    "frac_T_c_nonpositive": 0.0,
    "n_queries": 300,
    "ratio": 1.5563227478541544,
    "ratio_upper95_onesided": 2.018394023073672
  },
  "portable-elm_penalty_decomposition": {
    "recal_recovery": 0.001733333333333309,
    "remean_recovery": -0.02516000000000007,
    "residual": 0.13607000000000002,
    "total_penalty": 0.11264333333333326
  },
  "portable-mlp_penalty_decomposition": {
    "recal_recovery": 0.00025999999999998247,
    "remean_recovery": -0.016273333333333362,
    "residual": 0.09418000000000004,
    "total_penalty": 0.07816666666666666
  },
  "portable_mlp_minus_muvera10240": {
    "lower95_onesided": -0.03644084367803545,
    "mean": -0.015320990855710488
  },
  "portable_mlp_minus_portable_elm": {
    "lower95_onesided": 0.06712752737815274,
    "mean": 0.08470260484617079
  }
}
```

### ANN leg: default

| arm | seed 1 | seed 2 | seed 3 | mean nDCG@10 |
|---|---:|---:|---:|---:|
| percorpus-mlp | 0.37577 | 0.38897 | 0.37550 | 0.38008 |
| percorpus-elm | 0.34972 | 0.31471 | 0.32607 | 0.33017 |
| portable-mlp | 0.32341 | 0.31164 | 0.30951 | 0.31485 |
| portable-elm | 0.25138 | 0.23012 | 0.21527 | 0.23226 |
| portable-mlp-remean | 0.28847 | 0.30307 | 0.31527 | 0.30227 |
| portable-elm-remean | 0.22414 | 0.22398 | 0.18644 | 0.21152 |
| portable-mlp-recal | 0.31923 | 0.31208 | 0.31069 | 0.31400 |
| portable-elm-recal | 0.25526 | 0.22729 | 0.20243 | 0.22833 |
| portable-mlp-basis | 0.31531 | 0.33760 | 0.30050 | 0.31780 |
| muvera-20,5,16 (muvera r20 h5 p16 = 10240 dims) | — | — | — | 0.35957 |
| muvera-4,5,16 (muvera r4 h5 p16 = 2048 dims) | — | — | — | 0.25044 |
| muvera-20,2,32 (muvera r20 h2 p32 = 2560 dims) | — | — | — | 0.29001 |

```
{
  "portability": {
    "T_c": 0.049915591284852484,
    "T_c_lower95": 0.025439204351249464,
    "delta_c": 0.06522781028985374,
    "delta_c_ci90": [
      0.03907548003225199,
      0.09257027408667251
    ],
    "frac_T_c_nonpositive": 0.0004,
    "n_queries": 300,
    "ratio": 1.3067622482446268,
    "ratio_upper95_onesided": 2.2366212156316454
  },
  "portable-elm_penalty_decomposition": {
    "recal_recovery": -0.003930000000000017,
    "remean_recovery": -0.020736666666666653,
    "residual": 0.12257666666666667,
    "total_penalty": 0.09791
  },
  "portable-mlp_penalty_decomposition": {
    "recal_recovery": -0.0008533333333332616,
    "remean_recovery": -0.01258333333333328,
    "residual": 0.07866333333333325,
    "total_penalty": 0.06522666666666671
  },
  "portable_mlp_minus_muvera10240": {
    "lower95_onesided": -0.08017893890566395,
    "mean": -0.04472075990783885
  },
  "portable_mlp_minus_portable_elm": {
    "lower95_onesided": 0.057276459623186254,
    "mean": 0.08259540199839013
  }
}
```

## arguana

### ANN leg: exact

| arm | seed 1 | seed 2 | seed 3 | mean nDCG@10 |
|---|---:|---:|---:|---:|
| percorpus-mlp | 0.40563 | 0.40802 | 0.40097 | 0.40487 |
| percorpus-elm | 0.30778 | 0.31387 | 0.30408 | 0.30858 |
| portable-mlp | 0.34783 | 0.35000 | 0.35232 | 0.35005 |
| portable-elm | 0.30045 | 0.31198 | 0.29941 | 0.30395 |
| portable-mlp-remean | 0.35860 | 0.35949 | 0.35668 | 0.35826 |
| portable-elm-remean | 0.30143 | 0.30871 | 0.30859 | 0.30624 |
| portable-mlp-recal | 0.34584 | 0.34805 | 0.35176 | 0.34855 |
| portable-elm-recal | 0.29586 | 0.30665 | 0.29304 | 0.29852 |
| portable-mlp-basis | 0.34161 | 0.35093 | 0.34220 | 0.34491 |
| muvera-20,5,16 (muvera r20 h5 p16 = 10240 dims) | — | — | — | 0.34758 |
| muvera-4,5,16 (muvera r4 h5 p16 = 2048 dims) | — | — | — | 0.25916 |
| muvera-20,2,32 (muvera r20 h2 p32 = 2560 dims) | — | — | — | 0.33656 |

```
{
  "portability": {
    "T_c": 0.09629804105605516,
    "T_c_lower95": 0.08876730310627096,
    "delta_c": 0.05482366165491359,
    "delta_c_ci90": [
      0.04739735295836335,
      0.06250990417157179
    ],
    "frac_T_c_nonpositive": 0.0,
    "n_queries": 1401,
    "ratio": 0.569312325086662,
    "ratio_upper95_onesided": 0.643563561432688
  },
  "portable-elm_penalty_decomposition": {
    "recal_recovery": -0.005429999999999935,
    "remean_recovery": 0.0022966666666666136,
    "residual": 0.007763333333333344,
    "total_penalty": 0.004630000000000023
  },
  "portable-mlp_penalty_decomposition": {
    "recal_recovery": -0.0015000000000000013,
    "remean_recovery": 0.008206666666666695,
    "residual": 0.048116666666666696,
    "total_penalty": 0.05482333333333339
  },
  "portable_mlp_minus_muvera10240": {
    "lower95_onesided": -0.007007768060361555,
    "mean": 0.0024748433638101274
  },
  "portable_mlp_minus_portable_elm": {
    "lower95_onesided": 0.039443293683735926,
    "mean": 0.04610484599769424
  }
}
```

### ANN leg: default

| arm | seed 1 | seed 2 | seed 3 | mean nDCG@10 |
|---|---:|---:|---:|---:|
| percorpus-mlp | 0.40139 | 0.40235 | 0.39947 | 0.40107 |
| percorpus-elm | 0.28151 | 0.28747 | 0.28423 | 0.28440 |
| portable-mlp | 0.31918 | 0.31954 | 0.30567 | 0.31480 |
| portable-elm | 0.27517 | 0.29250 | 0.27638 | 0.28135 |
| portable-mlp-remean | 0.34138 | 0.34111 | 0.32603 | 0.33617 |
| portable-elm-remean | 0.27420 | 0.28535 | 0.29377 | 0.28444 |
| portable-mlp-recal | 0.31059 | 0.31285 | 0.29875 | 0.30740 |
| portable-elm-recal | 0.27418 | 0.28665 | 0.26722 | 0.27602 |
| portable-mlp-basis | 0.31477 | 0.31887 | 0.30016 | 0.31127 |
| muvera-20,5,16 (muvera r20 h5 p16 = 10240 dims) | — | — | — | 0.34256 |
| muvera-4,5,16 (muvera r4 h5 p16 = 2048 dims) | — | — | — | 0.24964 |
| muvera-20,2,32 (muvera r20 h2 p32 = 2560 dims) | — | — | — | 0.33152 |

```
{
  "portability": {
    "T_c": 0.1166676322995214,
    "T_c_lower95": 0.10720949054127525,
    "delta_c": 0.08627472350902929,
    "delta_c_ci90": [
      0.07691373092723384,
      0.09570914797874162
    ],
    "frac_T_c_nonpositive": 0.0,
    "n_queries": 1401,
    "ratio": 0.7394915094148458,
    "ratio_upper95_onesided": 0.8180200492390455
  },
  "portable-elm_penalty_decomposition": {
    "recal_recovery": -0.005333333333333357,
    "remean_recovery": 0.0030899999999999817,
    "residual": 0.005296666666666727,
    "total_penalty": 0.0030533333333333523
  },
  "portable-mlp_penalty_decomposition": {
    "recal_recovery": -0.007399999999999962,
    "remean_recovery": 0.02137666666666671,
    "residual": 0.07229666666666656,
    "total_penalty": 0.08627333333333331
  },
  "portable_mlp_minus_muvera10240": {
    "lower95_onesided": -0.038402462129630686,
    "mean": -0.027760489845218523
  },
  "portable_mlp_minus_portable_elm": {
    "lower95_onesided": 0.025468232448102243,
    "mean": 0.033447041008937965
  }
}
```

## Out-of-matrix legacy replication control (nfcorpus / MLP / seed 42 / center:false both ends)
nDCG@10 = 0.25524 vs previously recorded 0.25524 (diff +0.00000; the prior control table drifted 0.25534 vs 0.25524, so a tolerance of ±0.002 is the reading aid, not a gate)

## Preflight — calibration z = (maxsim(docs, sample) - mean) / std on target docs

| artifact | corpus | docs | mean z | sd z | p5 | p50 | p95 | frac<0 | frac<-2 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| arguana-elm-s1 | arguana | 2000 | 0.0018 | 1.0021 | -1.196 | -0.170 | 1.849 | 0.5935 | 0.0010 |
| arguana-mlp-s1 | arguana | 2000 | 0.0015 | 1.0018 | -1.196 | -0.170 | 1.848 | 0.5937 | 0.0009 |
| nfcorpus-elm-s1 | nfcorpus | 2000 | -0.0079 | 0.9948 | -1.180 | -0.183 | 1.882 | 0.6067 | 0.0006 |
| nfcorpus-mlp-s1 | nfcorpus | 2000 | -0.0086 | 0.9938 | -1.180 | -0.184 | 1.879 | 0.6071 | 0.0005 |
| portable-elm-s1 | arguana | 2000 | -0.1069 | 0.9381 | -1.373 | -0.213 | 1.485 | 0.6066 | 0.0034 |
| portable-elm-s1 | nfcorpus | 2000 | -0.0108 | 0.8059 | -1.079 | -0.104 | 1.317 | 0.5622 | 0.0003 |
| portable-elm-s1 | scifact | 2000 | 0.0475 | 0.7806 | -0.996 | -0.039 | 1.324 | 0.5238 | 0.0002 |
| portable-mlp-basis-s1 | arguana | 2000 | -0.1108 | 0.9351 | -1.373 | -0.216 | 1.477 | 0.6085 | 0.0034 |
| portable-mlp-basis-s1 | nfcorpus | 2000 | -0.0189 | 0.8035 | -1.086 | -0.111 | 1.304 | 0.5666 | 0.0004 |
| portable-mlp-basis-s1 | scifact | 2000 | 0.0342 | 0.7734 | -1.004 | -0.050 | 1.297 | 0.5307 | 0.0002 |
| portable-mlp-s1 | arguana | 2000 | -0.1071 | 0.9380 | -1.373 | -0.213 | 1.484 | 0.6067 | 0.0034 |
| portable-mlp-s1 | nfcorpus | 2000 | -0.0110 | 0.8058 | -1.079 | -0.104 | 1.316 | 0.5624 | 0.0003 |
| portable-mlp-s1 | scifact | 2000 | 0.0473 | 0.7806 | -0.996 | -0.039 | 1.324 | 0.5240 | 0.0002 |
| scifact-elm-s1 | scifact | 2000 | 0.0017 | 0.9988 | -1.212 | -0.154 | 1.797 | 0.5909 | 0.0023 |
| scifact-mlp-s1 | scifact | 2000 | 0.0020 | 0.9991 | -1.212 | -0.154 | 1.798 | 0.5908 | 0.0023 |

## Artifacts

| artifact | data | n | type | seed | epoch/loss | wall s | peak VRAM GB | center key | sample rank | cond |
|---|---|---:|---|---:|---|---:|---:|---|---:|---:|
| arguana-elm-s1 | target:arguana | 8674 | elm | 1 | None/0.00000 | 88.5 | 11.302 | yes | 128 | 11.3 |
| arguana-elm-s2 | target:arguana | 8674 | elm | 2 | None/0.00000 | 87.3 | 11.302 | yes | 128 | 11.3 |
| arguana-elm-s3 | target:arguana | 8674 | elm | 3 | None/0.00000 | 90.1 | 11.302 | yes | 128 | 11.4 |
| arguana-mlp-s1 | target:arguana | 8674 | mlp | 1 | 100/0.07870 | 181.2 | 10.316 | yes | 128 | 11.3 |
| arguana-mlp-s2 | target:arguana | 8674 | mlp | 2 | 100/0.07857 | 179.5 | 10.316 | yes | 128 | 11.3 |
| arguana-mlp-s3 | target:arguana | 8674 | mlp | 3 | 100/0.07882 | 177.2 | 10.316 | yes | 128 | 11.4 |
| legacy-nfcorpus-mlp-s42 | target:nfcorpus | 3633 | mlp | 42 | 96/0.04652 | 79.7 | 4.873 | no | 128 | 18.4 |
| nfcorpus-elm-s1 | target:nfcorpus | 3633 | elm | 1 | None/0.00000 | 41.4 | 5.308 | yes | 128 | 12.5 |
| nfcorpus-elm-s2 | target:nfcorpus | 3633 | elm | 2 | None/0.00000 | 38.1 | 5.308 | yes | 128 | 12.7 |
| nfcorpus-elm-s3 | target:nfcorpus | 3633 | elm | 3 | None/0.00000 | 40.3 | 5.308 | yes | 128 | 12.6 |
| nfcorpus-mlp-s1 | target:nfcorpus | 3633 | mlp | 1 | 100/0.06906 | 80.6 | 4.873 | yes | 128 | 12.5 |
| nfcorpus-mlp-s2 | target:nfcorpus | 3633 | mlp | 2 | 100/0.06867 | 82.6 | 4.873 | yes | 128 | 12.7 |
| nfcorpus-mlp-s3 | target:nfcorpus | 3633 | mlp | 3 | 100/0.06827 | 81.8 | 4.873 | yes | 128 | 12.6 |
| portable-elm-s1 | source:draw8192 | 8192 | elm | 1 | None/0.00000 | 77.2 | 10.997 | yes | 128 | 8.5 |
| portable-elm-s2 | source:draw8192 | 8192 | elm | 2 | None/0.00000 | 78.5 | 10.997 | yes | 128 | 8.5 |
| portable-elm-s3 | source:draw8192 | 8192 | elm | 3 | None/0.00000 | 78.5 | 10.997 | yes | 128 | 8.6 |
| portable-mlp-basis-s1 | source:draw3101 | 3101 | mlp | 1 | 100/0.11056 | 67.3 | 3.889 | yes | 128 | 8.6 |
| portable-mlp-basis-s2 | source:draw3101 | 3101 | mlp | 2 | 100/0.11036 | 66.3 | 3.889 | yes | 128 | 8.6 |
| portable-mlp-basis-s3 | source:draw3101 | 3101 | mlp | 3 | 100/0.11054 | 66.9 | 3.889 | yes | 128 | 8.6 |
| portable-mlp-s1 | source:draw8192 | 8192 | mlp | 1 | 100/0.11443 | 169.9 | 10.01 | yes | 128 | 8.5 |
| portable-mlp-s2 | source:draw8192 | 8192 | mlp | 2 | 100/0.11375 | 168.7 | 10.01 | yes | 128 | 8.5 |
| portable-mlp-s3 | source:draw8192 | 8192 | mlp | 3 | 100/0.11414 | 171.7 | 10.01 | yes | 128 | 8.6 |
| scifact-elm-s1 | target:scifact | 5183 | elm | 1 | None/0.00000 | 56.9 | 7.362 | yes | 128 | 12.4 |
| scifact-elm-s2 | target:scifact | 5183 | elm | 2 | None/0.00000 | 54.7 | 7.362 | yes | 128 | 12.4 |
| scifact-elm-s3 | target:scifact | 5183 | elm | 3 | None/0.00000 | 56.6 | 7.362 | yes | 128 | 12.4 |
| scifact-mlp-s1 | target:scifact | 5183 | mlp | 1 | 100/0.08689 | 113.0 | 6.739 | yes | 128 | 12.4 |
| scifact-mlp-s2 | target:scifact | 5183 | mlp | 2 | 100/0.08662 | 115.4 | 6.739 | yes | 128 | 12.4 |
| scifact-mlp-s3 | target:scifact | 5183 | mlp | 3 | 100/0.08633 | 113.3 | 6.739 | yes | 128 | 12.4 |

## All cells

| cell | ann (effective) | components | nDCG@10 | MAP@10 | R@10 | P@10 | q<10 | center | index s | search s |
|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| arguana--muvera-20,2,32--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.33152 | 0.26375 | 0.55032 | 0.05503 | 0 | none | 45.17 | 2.55 |
| arguana--muvera-20,2,32--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.33656 | 0.26739 | 0.56031 | 0.05603 | 0 | none | 42.35 | 1.78 |
| arguana--muvera-20,5,16--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.34256 | 0.27225 | 0.57102 | 0.05710 | 0 | none | 41.5 | 11.75 |
| arguana--muvera-20,5,16--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.34758 | 0.27554 | 0.58173 | 0.05817 | 0 | none | 37.93 | 3.52 |
| arguana--muvera-4,5,16--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.24964 | 0.19700 | 0.42041 | 0.04204 | 0 | none | 23.67 | 2.35 |
| arguana--muvera-4,5,16--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.25916 | 0.20322 | 0.44111 | 0.04411 | 0 | none | 22.57 | 1.44 |
| arguana--percorpus-elm--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.28151 | 0.22678 | 0.45967 | 0.04597 | 0 | collection:66d16091 | 23.11 | 2.39 |
| arguana--percorpus-elm--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.30778 | 0.24420 | 0.51392 | 0.05139 | 0 | collection:66d16091 | 22.13 | 1.86 |
| arguana--percorpus-elm--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.28747 | 0.23010 | 0.47323 | 0.04732 | 0 | collection:66d16091 | 23.3 | 2.47 |
| arguana--percorpus-elm--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.31387 | 0.24812 | 0.52819 | 0.05282 | 0 | collection:66d16091 | 22.16 | 1.96 |
| arguana--percorpus-elm--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.28423 | 0.22454 | 0.47823 | 0.04782 | 0 | collection:66d16091 | 23.25 | 2.27 |
| arguana--percorpus-elm--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.30408 | 0.23781 | 0.52106 | 0.05211 | 0 | collection:66d16091 | 22.16 | 1.88 |
| arguana--percorpus-mlp--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.40139 | 0.32950 | 0.63241 | 0.06324 | 0 | collection:66d16091 | 23.01 | 2.38 |
| arguana--percorpus-mlp--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.40563 | 0.33265 | 0.64026 | 0.06403 | 0 | collection:66d16091 | 21.95 | 1.85 |
| arguana--percorpus-mlp--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.40235 | 0.33001 | 0.63597 | 0.06360 | 0 | collection:66d16091 | 23.15 | 2.29 |
| arguana--percorpus-mlp--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.40802 | 0.33338 | 0.64954 | 0.06495 | 0 | collection:66d16091 | 22.1 | 1.88 |
| arguana--percorpus-mlp--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.39947 | 0.32620 | 0.63526 | 0.06353 | 0 | collection:66d16091 | 23.13 | 2.32 |
| arguana--percorpus-mlp--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.40097 | 0.32654 | 0.64097 | 0.06410 | 0 | collection:66d16091 | 22.32 | 1.91 |
| arguana--portable-elm--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.27517 | 0.22249 | 0.44611 | 0.04461 | 0 | collection:3256d659 | 23.11 | 2.34 |
| arguana--portable-elm--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.30045 | 0.24173 | 0.49036 | 0.04904 | 0 | collection:3256d659 | 22.09 | 1.88 |
| arguana--portable-elm--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.29250 | 0.23438 | 0.48037 | 0.04804 | 0 | collection:3256d659 | 23.14 | 2.46 |
| arguana--portable-elm--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.31198 | 0.24832 | 0.51892 | 0.05189 | 0 | collection:3256d659 | 22.11 | 1.88 |
| arguana--portable-elm--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.27638 | 0.21882 | 0.46253 | 0.04625 | 0 | collection:3256d659 | 23.14 | 2.29 |
| arguana--portable-elm--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.29941 | 0.23682 | 0.50321 | 0.05032 | 0 | collection:3256d659 | 22.11 | 1.87 |
| arguana--portable-elm-recal--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.27418 | 0.22232 | 0.44254 | 0.04425 | 0 | collection:3256d659 | 23.01 | 2.4 |
| arguana--portable-elm-recal--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.29586 | 0.23722 | 0.48608 | 0.04861 | 0 | collection:3256d659 | 22.11 | 1.94 |
| arguana--portable-elm-recal--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.28665 | 0.22925 | 0.47252 | 0.04725 | 0 | collection:3256d659 | 23.25 | 2.46 |
| arguana--portable-elm-recal--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.30665 | 0.24400 | 0.51035 | 0.05103 | 0 | collection:3256d659 | 22.08 | 1.87 |
| arguana--portable-elm-recal--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.26722 | 0.21167 | 0.44682 | 0.04468 | 0 | collection:3256d659 | 23.15 | 2.47 |
| arguana--portable-elm-recal--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.29304 | 0.23097 | 0.49536 | 0.04954 | 0 | collection:3256d659 | 22.17 | 1.88 |
| arguana--portable-elm-remean--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.27420 | 0.21883 | 0.45325 | 0.04532 | 0 | collection:4aca0133 | 22.96 | 2.33 |
| arguana--portable-elm-remean--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.30143 | 0.24036 | 0.49893 | 0.04989 | 0 | collection:4aca0133 | 22.06 | 1.89 |
| arguana--portable-elm-remean--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.28535 | 0.22624 | 0.47680 | 0.04768 | 0 | collection:4aca0133 | 23.11 | 2.35 |
| arguana--portable-elm-remean--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.30871 | 0.24316 | 0.52106 | 0.05211 | 0 | collection:4aca0133 | 22.01 | 1.91 |
| arguana--portable-elm-remean--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.29377 | 0.23322 | 0.49036 | 0.04904 | 0 | collection:4aca0133 | 23.19 | 2.28 |
| arguana--portable-elm-remean--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.30859 | 0.24400 | 0.51820 | 0.05182 | 0 | collection:4aca0133 | 22.19 | 1.87 |
| arguana--portable-mlp--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.31918 | 0.25732 | 0.51892 | 0.05189 | 0 | collection:3256d659 | 23.13 | 2.44 |
| arguana--portable-mlp--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.34783 | 0.28064 | 0.56602 | 0.05660 | 0 | collection:3256d659 | 22.06 | 1.91 |
| arguana--portable-mlp--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.31954 | 0.25645 | 0.52463 | 0.05246 | 0 | collection:3256d659 | 23.14 | 2.36 |
| arguana--portable-mlp--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.35000 | 0.28239 | 0.56959 | 0.05696 | 0 | collection:3256d659 | 22.21 | 1.87 |
| arguana--portable-mlp--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.30567 | 0.24479 | 0.50250 | 0.05025 | 0 | collection:3256d659 | 23.21 | 2.33 |
| arguana--portable-mlp--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.35232 | 0.28313 | 0.57673 | 0.05767 | 0 | collection:3256d659 | 22.22 | 1.97 |
| arguana--portable-mlp-basis--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.31477 | 0.25471 | 0.50964 | 0.05096 | 0 | collection:e626e97f | 23.09 | 2.34 |
| arguana--portable-mlp-basis--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.34161 | 0.27569 | 0.55603 | 0.05560 | 0 | collection:e626e97f | 22.12 | 1.92 |
| arguana--portable-mlp-basis--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.31887 | 0.25818 | 0.51535 | 0.05153 | 0 | collection:e626e97f | 23.33 | 2.39 |
| arguana--portable-mlp-basis--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.35093 | 0.28229 | 0.57388 | 0.05739 | 0 | collection:e626e97f | 22.2 | 1.9 |
| arguana--portable-mlp-basis--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.30016 | 0.24306 | 0.48537 | 0.04854 | 0 | collection:e626e97f | 23.21 | 2.4 |
| arguana--portable-mlp-basis--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.34220 | 0.27620 | 0.55675 | 0.05567 | 0 | collection:e626e97f | 22.06 | 1.86 |
| arguana--portable-mlp-recal--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.31059 | 0.25090 | 0.50321 | 0.05032 | 0 | collection:3256d659 | 23.0 | 2.45 |
| arguana--portable-mlp-recal--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.34584 | 0.27910 | 0.56246 | 0.05625 | 0 | collection:3256d659 | 22.13 | 1.9 |
| arguana--portable-mlp-recal--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.31285 | 0.25011 | 0.51677 | 0.05168 | 0 | collection:3256d659 | 23.08 | 2.32 |
| arguana--portable-mlp-recal--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.34805 | 0.28047 | 0.56745 | 0.05675 | 0 | collection:3256d659 | 22.12 | 1.89 |
| arguana--portable-mlp-recal--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.29875 | 0.23926 | 0.49108 | 0.04911 | 0 | collection:3256d659 | 23.22 | 2.43 |
| arguana--portable-mlp-recal--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.35176 | 0.28290 | 0.57530 | 0.05753 | 0 | collection:3256d659 | 22.32 | 1.93 |
| arguana--portable-mlp-remean--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.34138 | 0.27490 | 0.55675 | 0.05567 | 0 | collection:4aca0133 | 22.92 | 2.37 |
| arguana--portable-mlp-remean--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.35860 | 0.28899 | 0.58458 | 0.05846 | 0 | collection:4aca0133 | 21.99 | 1.81 |
| arguana--portable-mlp-remean--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.34111 | 0.27683 | 0.54961 | 0.05496 | 0 | collection:4aca0133 | 23.24 | 2.4 |
| arguana--portable-mlp-remean--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.35949 | 0.29166 | 0.57959 | 0.05796 | 0 | collection:4aca0133 | 22.12 | 1.95 |
| arguana--portable-mlp-remean--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=222 nprobe=14 | 0.32603 | 0.26287 | 0.52962 | 0.05296 | 0 | collection:4aca0133 | 23.19 | 2.47 |
| arguana--portable-mlp-remean--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.35668 | 0.28799 | 0.57816 | 0.05782 | 0 | collection:4aca0133 | 22.33 | 1.92 |
| nfcorpus--legacy-mlp-center-false--s42--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.25524 | 0.08474 | 0.11323 | 0.19071 | 117 | none | 10.32 | 0.21 |
| nfcorpus--muvera-20,2,32--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.18455 | 0.05572 | 0.08121 | 0.14087 | 0 | none | 21.72 | 0.21 |
| nfcorpus--muvera-20,5,16--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.24015 | 0.08140 | 0.11516 | 0.17678 | 0 | none | 17.63 | 0.38 |
| nfcorpus--muvera-4,5,16--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.16409 | 0.04999 | 0.07646 | 0.11827 | 0 | none | 10.99 | 0.2 |
| nfcorpus--percorpus-elm--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.21094 | 0.06243 | 0.09091 | 0.16440 | 0 | collection:a12dad9c | 10.87 | 0.23 |
| nfcorpus--percorpus-elm--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.21617 | 0.06415 | 0.09818 | 0.16780 | 0 | collection:a12dad9c | 10.84 | 0.22 |
| nfcorpus--percorpus-elm--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.22230 | 0.07112 | 0.10507 | 0.16966 | 0 | collection:a12dad9c | 10.9 | 0.22 |
| nfcorpus--percorpus-mlp--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.27346 | 0.09337 | 0.12762 | 0.20341 | 0 | collection:a12dad9c | 10.95 | 0.22 |
| nfcorpus--percorpus-mlp--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.27865 | 0.09468 | 0.13523 | 0.20805 | 0 | collection:a12dad9c | 10.87 | 0.23 |
| nfcorpus--percorpus-mlp--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.27609 | 0.09354 | 0.13243 | 0.20372 | 0 | collection:a12dad9c | 10.83 | 0.21 |
| nfcorpus--portable-elm--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.20825 | 0.06238 | 0.10443 | 0.15882 | 0 | collection:3256d659 | 10.79 | 0.23 |
| nfcorpus--portable-elm--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.21349 | 0.06937 | 0.09717 | 0.15820 | 0 | collection:3256d659 | 10.96 | 0.23 |
| nfcorpus--portable-elm--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.20317 | 0.06071 | 0.09056 | 0.14985 | 0 | collection:3256d659 | 10.68 | 0.22 |
| nfcorpus--portable-elm-recal--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.20821 | 0.06250 | 0.10439 | 0.15851 | 0 | collection:3256d659 | 10.86 | 0.22 |
| nfcorpus--portable-elm-recal--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.21298 | 0.06927 | 0.09704 | 0.15759 | 0 | collection:3256d659 | 10.71 | 0.21 |
| nfcorpus--portable-elm-recal--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.20305 | 0.06072 | 0.09059 | 0.14985 | 0 | collection:3256d659 | 10.88 | 0.21 |
| nfcorpus--portable-elm-remean--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.16969 | 0.04429 | 0.08191 | 0.13375 | 0 | collection:4f596304 | 10.75 | 0.22 |
| nfcorpus--portable-elm-remean--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.17753 | 0.05522 | 0.07896 | 0.13375 | 0 | collection:4f596304 | 10.81 | 0.21 |
| nfcorpus--portable-elm-remean--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.16775 | 0.04617 | 0.07929 | 0.12724 | 0 | collection:4f596304 | 10.83 | 0.22 |
| nfcorpus--portable-mlp--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.24143 | 0.08455 | 0.11853 | 0.16966 | 0 | collection:3256d659 | 10.68 | 0.22 |
| nfcorpus--portable-mlp--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.24133 | 0.08084 | 0.11805 | 0.17678 | 0 | collection:3256d659 | 10.89 | 0.2 |
| nfcorpus--portable-mlp--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.23686 | 0.07843 | 0.11526 | 0.17183 | 0 | collection:3256d659 | 10.91 | 0.22 |
| nfcorpus--portable-mlp-basis--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.23650 | 0.07831 | 0.11819 | 0.16904 | 0 | collection:e626e97f | 10.75 | 0.22 |
| nfcorpus--portable-mlp-basis--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.23553 | 0.07735 | 0.11338 | 0.17337 | 0 | collection:e626e97f | 10.74 | 0.23 |
| nfcorpus--portable-mlp-basis--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.23369 | 0.07506 | 0.11597 | 0.17214 | 0 | collection:e626e97f | 10.63 | 0.24 |
| nfcorpus--portable-mlp-recal--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.24143 | 0.08455 | 0.11853 | 0.16966 | 0 | collection:3256d659 | 10.88 | 0.23 |
| nfcorpus--portable-mlp-recal--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.24145 | 0.08084 | 0.11805 | 0.17678 | 0 | collection:3256d659 | 10.73 | 0.22 |
| nfcorpus--portable-mlp-recal--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.23688 | 0.07848 | 0.11526 | 0.17183 | 0 | collection:3256d659 | 10.78 | 0.24 |
| nfcorpus--portable-mlp-remean--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.21479 | 0.06946 | 0.11025 | 0.15789 | 0 | collection:4f596304 | 10.81 | 0.21 |
| nfcorpus--portable-mlp-remean--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.21214 | 0.06755 | 0.10453 | 0.15913 | 0 | collection:4f596304 | 10.79 | 0.21 |
| nfcorpus--portable-mlp-remean--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.20776 | 0.06389 | 0.11203 | 0.15418 | 0 | collection:4f596304 | 10.82 | 0.21 |
| scifact--muvera-20,2,32--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.29001 | 0.26540 | 0.34928 | 0.04067 | 0 | none | 32.64 | 0.31 |
| scifact--muvera-20,2,32--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.36595 | 0.32971 | 0.46078 | 0.05167 | 0 | none | 30.77 | 0.76 |
| scifact--muvera-20,5,16--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.35957 | 0.33334 | 0.42533 | 0.04967 | 0 | none | 27.36 | 1.54 |
| scifact--muvera-20,5,16--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.48130 | 0.44062 | 0.59200 | 0.06667 | 0 | none | 25.12 | 0.48 |
| scifact--muvera-4,5,16--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.25044 | 0.22965 | 0.29939 | 0.03533 | 0 | none | 15.85 | 0.25 |
| scifact--muvera-4,5,16--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.35250 | 0.31626 | 0.45200 | 0.05067 | 0 | none | 15.53 | 0.58 |
| scifact--percorpus-elm--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=1 | 0.34972 | 0.32209 | 0.41367 | 0.04767 | 0 | collection:e7fdcf65 | 15.36 | 0.26 |
| scifact--percorpus-elm--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.50513 | 0.45565 | 0.64200 | 0.07167 | 0 | collection:e7fdcf65 | 15.04 | 0.61 |
| scifact--percorpus-elm--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.31471 | 0.28718 | 0.38289 | 0.04433 | 0 | collection:e7fdcf65 | 15.66 | 0.27 |
| scifact--percorpus-elm--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.47955 | 0.43358 | 0.60578 | 0.06800 | 0 | collection:e7fdcf65 | 15.13 | 0.61 |
| scifact--percorpus-elm--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.32607 | 0.29740 | 0.39656 | 0.04633 | 0 | collection:e7fdcf65 | 15.67 | 0.28 |
| scifact--percorpus-elm--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.49708 | 0.45288 | 0.61894 | 0.07000 | 0 | collection:e7fdcf65 | 14.85 | 0.59 |
| scifact--percorpus-mlp--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=1 | 0.37577 | 0.34476 | 0.45489 | 0.05300 | 0 | collection:e7fdcf65 | 15.43 | 0.3 |
| scifact--percorpus-mlp--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.54805 | 0.50356 | 0.67056 | 0.07633 | 0 | collection:e7fdcf65 | 15.1 | 0.61 |
| scifact--percorpus-mlp--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.38897 | 0.35681 | 0.47206 | 0.05533 | 0 | collection:e7fdcf65 | 15.47 | 0.26 |
| scifact--percorpus-mlp--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.54687 | 0.50199 | 0.66639 | 0.07567 | 0 | collection:e7fdcf65 | 14.97 | 0.59 |
| scifact--percorpus-mlp--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.37550 | 0.34456 | 0.45156 | 0.05267 | 0 | collection:e7fdcf65 | 15.42 | 0.3 |
| scifact--percorpus-mlp--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.53753 | 0.49173 | 0.66056 | 0.07533 | 0 | collection:e7fdcf65 | 15.09 | 0.59 |
| scifact--portable-elm--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=1 | 0.25138 | 0.22624 | 0.31889 | 0.03700 | 0 | collection:3256d659 | 15.46 | 0.28 |
| scifact--portable-elm--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.37682 | 0.33337 | 0.49733 | 0.05633 | 0 | collection:3256d659 | 15.05 | 0.59 |
| scifact--portable-elm--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.23012 | 0.20438 | 0.29372 | 0.03467 | 0 | collection:3256d659 | 15.4 | 0.26 |
| scifact--portable-elm--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.39061 | 0.34457 | 0.52172 | 0.05900 | 0 | collection:3256d659 | 15.03 | 0.58 |
| scifact--portable-elm--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.21527 | 0.19046 | 0.27967 | 0.03267 | 0 | collection:3256d659 | 15.53 | 0.24 |
| scifact--portable-elm--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.37640 | 0.33105 | 0.50322 | 0.05767 | 0 | collection:3256d659 | 15.05 | 0.58 |
| scifact--portable-elm-recal--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=1 | 0.25526 | 0.22929 | 0.32556 | 0.03767 | 0 | collection:3256d659 | 15.52 | 0.26 |
| scifact--portable-elm-recal--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.37864 | 0.33576 | 0.49733 | 0.05633 | 0 | collection:3256d659 | 15.16 | 0.59 |
| scifact--portable-elm-recal--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.22729 | 0.20267 | 0.28789 | 0.03367 | 0 | collection:3256d659 | 15.35 | 0.26 |
| scifact--portable-elm-recal--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.39366 | 0.34628 | 0.52906 | 0.06000 | 0 | collection:3256d659 | 15.06 | 0.6 |
| scifact--portable-elm-recal--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.20243 | 0.18051 | 0.25750 | 0.03000 | 0 | collection:3256d659 | 15.62 | 0.26 |
| scifact--portable-elm-recal--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.37673 | 0.33218 | 0.49989 | 0.05733 | 0 | collection:3256d659 | 15.24 | 0.62 |
| scifact--portable-elm-remean--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=1 | 0.22414 | 0.20025 | 0.28500 | 0.03300 | 0 | collection:1592b039 | 15.45 | 0.3 |
| scifact--portable-elm-remean--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.35377 | 0.30733 | 0.48289 | 0.05433 | 0 | collection:1592b039 | 14.95 | 0.58 |
| scifact--portable-elm-remean--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.22398 | 0.20294 | 0.27444 | 0.03167 | 0 | collection:1592b039 | 15.34 | 0.24 |
| scifact--portable-elm-remean--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.36930 | 0.32658 | 0.48800 | 0.05500 | 0 | collection:1592b039 | 15.18 | 0.6 |
| scifact--portable-elm-remean--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.18644 | 0.16432 | 0.24339 | 0.02967 | 0 | collection:1592b039 | 15.59 | 0.26 |
| scifact--portable-elm-remean--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.34528 | 0.30423 | 0.45644 | 0.05233 | 0 | collection:1592b039 | 15.18 | 0.62 |
| scifact--portable-mlp--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=1 | 0.32341 | 0.29682 | 0.39006 | 0.04467 | 0 | collection:3256d659 | 15.75 | 0.26 |
| scifact--portable-mlp--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.46689 | 0.42527 | 0.58089 | 0.06500 | 0 | collection:3256d659 | 15.18 | 0.65 |
| scifact--portable-mlp--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.31164 | 0.28227 | 0.38200 | 0.04533 | 0 | collection:3256d659 | 15.4 | 0.32 |
| scifact--portable-mlp--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.46177 | 0.42279 | 0.56367 | 0.06367 | 0 | collection:3256d659 | 15.02 | 0.61 |
| scifact--portable-mlp--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.30951 | 0.28301 | 0.37672 | 0.04467 | 0 | collection:3256d659 | 15.45 | 0.26 |
| scifact--portable-mlp--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.46929 | 0.43050 | 0.57506 | 0.06433 | 0 | collection:3256d659 | 15.15 | 0.6 |
| scifact--portable-mlp-basis--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.31531 | 0.28906 | 0.37739 | 0.04467 | 0 | collection:e626e97f | 15.74 | 0.29 |
| scifact--portable-mlp-basis--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.47633 | 0.43349 | 0.59006 | 0.06633 | 0 | collection:e626e97f | 15.17 | 0.61 |
| scifact--portable-mlp-basis--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.33760 | 0.31146 | 0.40078 | 0.04633 | 0 | collection:e626e97f | 15.67 | 0.27 |
| scifact--portable-mlp-basis--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.46744 | 0.42993 | 0.56356 | 0.06333 | 0 | collection:e626e97f | 15.41 | 0.6 |
| scifact--portable-mlp-basis--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.30050 | 0.26908 | 0.37744 | 0.04367 | 0 | collection:e626e97f | 15.6 | 0.26 |
| scifact--portable-mlp-basis--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.45175 | 0.40748 | 0.57256 | 0.06467 | 0 | collection:e626e97f | 15.15 | 0.6 |
| scifact--portable-mlp-recal--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=1 | 0.31923 | 0.29289 | 0.38589 | 0.04400 | 0 | collection:3256d659 | 15.52 | 0.25 |
| scifact--portable-mlp-recal--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.46693 | 0.42532 | 0.58089 | 0.06500 | 0 | collection:3256d659 | 14.98 | 0.58 |
| scifact--portable-mlp-recal--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.31208 | 0.28282 | 0.38200 | 0.04533 | 0 | collection:3256d659 | 15.41 | 0.26 |
| scifact--portable-mlp-recal--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.46220 | 0.42335 | 0.56367 | 0.06367 | 0 | collection:3256d659 | 15.08 | 0.63 |
| scifact--portable-mlp-recal--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.31069 | 0.28449 | 0.37672 | 0.04467 | 0 | collection:3256d659 | 15.49 | 0.29 |
| scifact--portable-mlp-recal--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.46960 | 0.43086 | 0.57506 | 0.06433 | 0 | collection:3256d659 | 15.12 | 0.6 |
| scifact--portable-mlp-remean--s1--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=1 | 0.28847 | 0.25985 | 0.36006 | 0.04300 | 0 | collection:1592b039 | 15.34 | 0.28 |
| scifact--portable-mlp-remean--s1--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.44461 | 0.39864 | 0.57172 | 0.06400 | 0 | collection:1592b039 | 15.09 | 0.62 |
| scifact--portable-mlp-remean--s2--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.30307 | 0.27132 | 0.38189 | 0.04533 | 0 | collection:1592b039 | 15.64 | 0.26 |
| scifact--portable-mlp-remean--s2--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.44834 | 0.40057 | 0.58033 | 0.06567 | 0 | collection:1592b039 | 15.21 | 0.59 |
| scifact--portable-mlp-remean--s3--default | default (default-ivf) | auto → IndexIVFFlat nlist=132 nprobe=8 | 0.31527 | 0.28890 | 0.38183 | 0.04533 | 0 | collection:1592b039 | 15.48 | 0.26 |
| scifact--portable-mlp-remean--s3--exact | exact (exact) | IDMap,Flat → IndexIDMap(IndexFlat) | 0.45618 | 0.41736 | 0.56406 | 0.06300 | 0 | collection:1592b039 | 15.18 | 0.61 |

## Honest notes

Development-pilot numbers over development corpora; not a shipping benchmark.

† nprobe shown as txtai's search-time rule round(nlist/16): these cells were recorded by harness revision 1, whose index descriptor was captured before search (faiss default nprobe=1 in the string); the searches themselves ran at txtai's value. Later cells record `nprobe_used` directly.
