import sys, json, glob, importlib.util
from multiprocessing import Pool
sys.path.insert(0,'.')
import wercore as W
base='raw/'
spec=importlib.util.spec_from_file_location('wer_pkg', base+'dl/WER/Python Folder Configurations/python-word-error-rate-master/word_error_rate.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.print_to_html=lambda *a,**k: None   # skip the HTML diff output only
T=json.load(open('tables123.json')); LT=base+'dl2/Google_Files_All_New/'
jobs=[]
for i,o in T.items():
    if i=='26.6_n': continue
    g=glob.glob(LT+i+'_ref.txt') or glob.glob(LT+i+'__ref.txt')
    for nm in ['LT','DICT','MT']:
        if o[nm]: jobs.append((i,nm,g[0],base+o[nm]['file'],o[nm]['wer']))
jobs.sort(key=lambda j:-len(open(j[2],errors='ignore').read()))
def run(j):
    i,nm,r,h,jw=j
    rr=W.stats(r)['words']; hh=W.stats(h)['words']
    return (i,nm,m.get_word_error_rate(rr,hh)/100.0,jw)
if __name__=='__main__':
    with Pool(2) as p:
        out=[]
        for x in p.imap_unordered(run,jobs):
            out.append(x); json.dump(out,open('pywer_results.json','w'))
    print('done',len(out),max(abs(a-b) for _,_,a,b in out))
