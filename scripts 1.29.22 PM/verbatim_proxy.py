import sys, json, re, glob, pandas as pd, numpy as np, jiwer; sys.path.insert(0,'.')
import wercore as W
from scipy import stats
base='raw/dl2/Google_Files_All_New/'
df=pd.read_csv('recomputed_all_pairs.csv',index_col=0); v=df[df.in_paper==True]
FILL={'um','uh','er','erm','ah','hmm','mm','uhm','umm','uhh','eh','mhm'}
def disfl(w): # immediate word repeats (false starts/repetitions proxy)
    return sum(1 for a,b in zip(w,w[1:]) if a==b)
rows=[]
for k in v.index:
    r=W.stats(base+v.loc[k,'ref'])['words']; h=W.stats(base+v.loc[k,'hypo'])['words']
    r2=[x for x in r if x not in FILL]; h2=[x for x in h if x not in FILL]
    w0=jiwer.process_words(' '.join(r),' '.join(h)); w1=jiwer.process_words(' '.join(r2),' '.join(h2))
    # remove repeats too
    def dedup(w): return [x for i,x in enumerate(w) if i==0 or x!=w[i-1]]
    r3=dedup(r2); h3=dedup(h2); w2=jiwer.process_words(' '.join(r3),' '.join(h3))
    rows.append(dict(id=k,n_r=len(r),n_h=len(h),fill_r=sum(x in FILL for x in r)/len(r)*1000,fill_h=sum(x in FILL for x in h)/len(h)*1000,
      rep_r=disfl(r)/len(r)*1000,rep_h=disfl(h)/len(h)*1000,wer=w0.wer,wer_nofill=w1.wer,wer_clean=w2.wer,S=w0.substitutions,D=w0.deletions,I=w0.insertions))
o=pd.DataFrame(rows).set_index('id'); o.to_csv('verbatim_proxy.csv')
print(o[['fill_r','fill_h','rep_r','rep_h','wer','wer_nofill','wer_clean']].describe().loc[['mean','50%']].round(4))
print('mean WER',o.wer.mean(),'nofill',o.wer_nofill.mean(),'clean',o.wer_clean.mean())
print('wilcoxon wer vs clean',stats.wilcoxon(o.wer,o.wer_clean))
print('S,D,I totals',o.S.sum(),o.D.sum(),o.I.sum(), 'shares', (o[['S','D','I']].sum()/o[['S','D','I']].sum().sum()).round(3).to_dict())
print('hyp has more words than ref in',(o.n_h>o.n_r).sum(),'of',len(o))
