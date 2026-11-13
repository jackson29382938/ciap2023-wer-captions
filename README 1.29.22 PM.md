# CIAP2023 captions: human vs automated transcripts (data and code)

Data and analysis code for the paper *Comparison of in situ human and post hoc automated transcriptions of talks at a scientific conference* (Jackson, Miller, Galvin, Landsberger, Reiss, Rubinstein, Ratnanather).

The talks were recorded at the 2023 Conference on Implantable Auditory Prostheses (CIAP2023). Real-time human captions were the reference; Live Transcribe, Microsoft Translator, and Live Transcribe with a custom dictionary generated the automated transcripts (hypotheses) in August to September 2024.

## What is here

| Path | Contents |
|---|---|
| `data/transcript_level_table.csv` | One row per transcript pair: word counts, mean word length, vowel counts, WER with substitution/deletion/insertion counts, the lower-bound check, and the mapping to the rows of the submitted Tables S1/S2. `in_verified_103` marks the 103 pairs used for the reported statistics. |
| `data/selected_talks_comparison.csv` | WER for Live Transcribe, Microsoft Translator, and Live Transcribe with the dictionary for the selected talks, with MAPSSWE p-values and segment counts, and the accent and clarity ratings. Row 97 is unverified (see the paper's Supplement). |
| `data/live_sessions.csv` | WER of live automated captions relative to live human captions, by session. |
| `data/filler_repetition_proxy.csv` | Filler and repetition rates per transcript pair and WER before and after removing them. |
| `data/python_wer_crosscheck.csv` | WER from the Python WER code and from JiWER for the verified selected comparisons. |
| `scripts/wercore.py` | Normalization (as in the original pipeline) and WER; word length is total letters divided by total words. |
| `scripts/mapsswe.py` | Independent MAPSSWE implementation (matched-pair segment test). |
| `scripts/wer_sanity_check.py` | Standing sanity test: WER lower bound, duplicate rows, vowels per word, word length. |
| other scripts | Pipeline that produced the tables above (`run_all.py`, `final_stats.py`, `tables123.py`, `live_vs_posthoc.py`, `verbatim_proxy.py`, `pywer_run.py`). Paths point to a `raw/` folder that is not included. |

## What is not here

Raw transcript text and speaker names are not included. The filenames in the tables are the randomized identifiers used in the paper. The talk recordings are public on the CIAP2023 website. The de-identified transcript pairs are available from the corresponding author on reasonable request.

## Reproducing the checks

```
pip install -r requirements.txt
python scripts/wer_sanity_check.py data/transcript_level_table_for_check.csv
```

`wer_sanity_check.py` expects the columns `n_r, n_h, wer, v_r, v_h, al_r, al_h`, which `data/transcript_level_table_for_check.csv` provides (the same table with the short column names that `final_stats.py` writes). It is expected to flag two word-length outliers: file `26.6_n` (a 63-word fragment) and file `40` (5.53 letters per word, a technical talk); no other check fails.

## Notes

- Hypothesis and reference columns in the submitted Supplement were interchanged and the submitted average word length used a per-line mean; both are corrected here (see the paper's Supplement, Table S3).
- p-values were recomputed with the independent MAPSSWE implementation; the submitted values came from NIST SCTK `sclite`.

## License

Code: MIT. Data tables: CC BY 4.0. (Suggested defaults; change if your institution requires otherwise.)
