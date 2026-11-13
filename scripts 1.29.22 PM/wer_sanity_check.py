#!/usr/bin/env python3
"""Standing sanity test for the WER table (packet item 2.2/2.3).

Usage: python wer_sanity_check.py recomputed_all_pairs.csv
Expected columns: n_r (reference words), n_h (hypothesis words), wer, v_r, v_h (vowel counts), al_r, al_h.
Checks every row for
  1. WER >= |N_hyp - N_ref| / N_ref   (every extra or missing word is an error)
  2. duplicated rows (identical hypothesis or reference statistics under different labels)
  3. vowels per word outside 1.2-2.4 (typical English is about 1.8)
  4. average word length outside 3.5-5.5 (technical talks run about 4.3-4.8)
Exit status 1 if any check fails, so it can be used in a test suite.
"""
import sys, pandas as pd
df = pd.read_csv(sys.argv[1], index_col=0)
bad = 0
lb = (df.n_h - df.n_r).abs() / df.n_r
for i in df[df.wer + 1e-9 < lb].index:
    print(f"LOWER BOUND: {i}: WER {df.wer[i]:.4f} < minimum {lb[i]:.4f}"); bad += 1
for side in ("r", "h"):
    key = [f"n_{side}", f"al_{side}", f"v_{side}"]
    dup = df[df.duplicated(key, keep=False)]
    for i in dup.index:
        print(f"DUPLICATE ({'reference' if side=='r' else 'hypothesis'}): {i}"); bad += 1
    vpw = df[f"v_{side}"] / df[f"n_{side}"]
    for i in df[(vpw < 1.2) | (vpw > 2.4)].index:
        print(f"VOWELS/WORD: {i} ({side}) = {vpw[i]:.2f}"); bad += 1
    al = df[f"al_{side}"]
    for i in df[(al < 3.5) | (al > 5.5)].index:
        print(f"WORD LENGTH: {i} ({side}) = {al[i]:.2f}"); bad += 1
print("OK" if not bad else f"{bad} problem(s)")
sys.exit(1 if bad else 0)
