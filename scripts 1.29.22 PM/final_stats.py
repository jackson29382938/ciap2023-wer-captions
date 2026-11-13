import sys,json,re,math,statistics as st
sys.path.insert(0,'.')
import numpy as np, pandas as pd
A=json.load(open('all_pairs.json')); P={int(k):v for k,v in json.load(open('paper.json')).items()}
M=json.load(open('map_paper_to_file.json'))   # file -> [paper rows]
rowof={}
for f,rows in M.items():
    for r in rows: rowof[r]=f
rowof[99]='53.1_r'
file2row={}
for r,f in rowof.items(): file2row.setdefault(f,[]).append(r)
df=pd.DataFrame(A).T
df['paper_rows']=[file2row.get(k,[]) for k in df.index]
df['in_paper']=df.paper_rows.apply(len)>0
df['paper_wer']=[P[r[0]]['wer'] if r else float('nan') for r in df.paper_rows]
df['wer_match']=(df.wer-df.paper_wer).abs()<5e-5
df['min_wer']=(df.n_r-df.n_h).abs()/df.n_r
df['bound_ok']=df.wer>=df.min_wer-1e-9
df['speaker']=df.index.str.replace('_Q&A','',regex=False)
df['is_qa']=df.index.str.endswith('Q&A')
df['type']=['Q&A' if k.endswith('Q&A') else 'industry' if k.startswith('00.') else 'intro' if k.startswith('0.') else 'panel/pre-recorded' if k.startswith('26.') else 'other' if k=='other_L' else 'podium' for k in df.index]
df.to_csv('recomputed_all_pairs.csv')
v=df[df.in_paper]
print("verified pairs:",len(v),"| WER matches paper to 4dp:",int(v.wer_match.sum()),"| mismatches:",int((~v.wer_match).sum()))
print("lower-bound violations among raw recomputed:",int((~df.bound_ok).sum()))
def summ(x,name):
    print(f"{name}: n={len(x)} mean={x.mean():.3f} sd={x.std(ddof=1):.3f} se={x.std(ddof=1)/math.sqrt(len(x)):.3f} median={x.median():.3f} min={x.min():.3f} max={x.max():.3f}")
summ(v.wer,"recomputed WER, 103 verified pairs")
summ(df.wer,"recomputed WER, all 123 raw pairs")
pw=pd.Series({r:P[r]['wer'] for r in P}); summ(pw,"paper S1/S2 WER as printed (106 rows)")
nm=v[~v.wer_match]; print("mismatch rows:",[(k,r,round(w,4),round(p,4)) for k,r,w,p in zip(nm.index,nm.paper_rows,nm.wer,nm.paper_wer)])
# corrected word length
print("token-weighted avg word length: ref mean=%.3f hyp mean=%.3f"%(v.al_r.mean(),v.al_h.mean()))
print("buggy line-avg: ref mean=%.3f hyp mean=%.3f"%(v.albug_r.mean(),v.albug_h.mean()))
print("blank-line share: ref=%.3f hyp=%.3f"%((v.blank_r/v.lines_r).mean(),(v.blank_h/v.lines_h).mean()))
print("vowels per word ref=%.3f hyp=%.3f"%((v.v_r/v.n_r).mean(),(v.v_h/v.n_h).mean()))
print("n speakers (verified):",v.speaker.nunique(),"talk/qa:",v.type.value_counts().to_dict())
print(v.groupby('type').wer.agg(['count','mean','median']))
