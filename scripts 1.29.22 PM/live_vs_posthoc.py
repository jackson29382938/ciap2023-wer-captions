import sys, json, re, jiwer; sys.path.insert(0,'.')
import wercore as W
d='raw/live_sessions/'
pairs=[('Day 1','DAY 1 CIAP HUMan','day 1 ciap ai'),('Day 2.1','day 2.1 CIAP human','day2.1 CIAP ai'),('Day 2.2','day 2.2 CIAP human','day 2.2 CIAP ai'),
('Day 2.3','day 2.3 human','day 2.3 ai'),('Day 2.4','day 2.4 human','day 2.4 ai'),('Day 3 (am)','day 3 morning human','day 3 morning ai'),('Day 3','day 3 human','day 3 ai'),('Day 4 pm','day 4 pm human','day 4 pm ai')]
def words(p):
    out=[]
    for l in open(d+p+'.txt',errors='ignore'):
        out+=W.norm_line(l).split()
    return out
res=[]
for nm,h,a in pairs:
    r=words(h); x=words(a)
    o=jiwer.process_words(' '.join(r),' '.join(x))
    res.append(dict(session=nm,n_human=len(r),n_ai=len(x),wer=o.wer,S=o.substitutions,D=o.deletions,I=o.insertions,lb=abs(len(x)-len(r))/len(r)))
    print(res[-1]['session'],len(r),len(x),round(o.wer,4),round(res[-1]['lb'],4))
tot=sum(r['n_human'] for r in res)
print('pooled WER', sum(r['wer']*r['n_human'] for r in res)/tot, 'mean',sum(r['wer'] for r in res)/len(res))
json.dump(res,open('live_sessions.json','w'),indent=1)
