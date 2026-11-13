import sys,json; sys.path.insert(0,'.')
import wercore as W, mapsswe as M
base='raw/'
LT=base+'dl2/Google_Files_All_New/'; DICT=base+'dl/WER/Transcript Files/'; MT=base+'dl3/MT_Unanalyzed/'
sel={ # id: (LT hypo, ref, dict path, MT path)
}
ids=['15','1','26.6_n','2','40','48','53.2_h','59','5','62','22','25','26.2_b','27','30','35','37','39','53.1_r','54']
import glob,os
def find(pattern):
    g=glob.glob(pattern); return g[0] if g else None
res={}
for i in ids:
    ltf=find(LT+i+'_hypo.txt') or find(LT+i+'_hypo.txt'); reff=find(LT+i+'_ref.txt') or find(LT+i+'__ref.txt')
    dh=find(DICT+'Google_Dictionary_Files_*/'+i+'_dict_hypo.txt') or find(DICT+'Google_Dictionary_Files_*/'+i+'_hypo.txt')
    mt=find(MT+'*/'+i+'_hypo.txt') or find(MT+'*/'+i+'_1hypo.txt')
    if i=='54': dh=find(DICT+'google dict files bottom and top/54_hypo.txt')  # note: in dict folder 54 is stored as 54_hypo
    r=W.stats(reff)['words']; out={}
    for nm,pth in [('LT',ltf),('DICT',dh),('MT',mt)]:
        if pth: h=W.stats(pth)['words']; out[nm]=dict(wer=W.wer(r,h)['wer'],n=len(h),file=pth.split('scratchpad/')[-1])
        else: out[nm]=None
    out['n_ref']=len(r)
    if out['LT'] and out['MT']: out['p_LT_MT']=M.mapsswe(r,W.stats(ltf)['words'],W.stats(mt)['words'])
    if out['LT'] and out['DICT']: out['p_LT_DICT']=M.mapsswe(r,W.stats(ltf)['words'],W.stats(dh)['words'])
    res[i]=out
json.dump(res,open('tables123.json','w'),indent=1)
print(f"{'id':8s} {'LT':>7s} {'MT':>7s} {'DICT':>7s} {'dMT?':>5s} {'chg%':>8s} {'p_LTMT':>8s} {'p_dict':>8s} nseg")
for i,o in res.items():
    lt,mt,d=o['LT']['wer'],o['MT']['wer'] if o['MT'] else float('nan'),o['DICT']['wer'] if o['DICT'] else float('nan')
    chg=100*(d-lt)/lt
    pm=o.get('p_LT_MT',{}).get('p',float('nan')); pd=o.get('p_LT_DICT',{}).get('p',float('nan'))
    print(f"{i:8s} {lt:7.4f} {mt:7.4f} {d:7.4f} {'MT<LT' if mt<lt else 'LT<MT':>5s} {chg:8.2f} {pm:8.4f} {pd:8.4f} {o.get('p_LT_MT',{}).get('n_seg')}")
