import sys, os, re, json, collections
sys.path.insert(0,'.')
import wercore as W
D='newfiles/'
fs=sorted(os.listdir(D))
pairs=collections.defaultdict(dict)
for f in fs:
    m=re.match(r'(.*?)_?(\d*)(hypo|ref)\.txt$',f)
    k=m.group(1).rstrip('_')+m.group(2)
    pairs[k][m.group(3)]=f
# paper rows
t=open('raw/manuscript/supplementary.tex').read()
rows=re.findall(r'^(\d+)\s*&\s*([\d.]+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*([\d.]+)\s*&\s*([\d.]+)\s*&\s*(\d+)\s*&\s*(\d+)\\\\',t,re.M)
paper={int(r[0]):dict(wer=float(r[1]),n_h=int(r[2]),n_r=int(r[3]),al_h=float(r[4]),al_r=float(r[5]),v_h=int(r[6]),v_r=int(r[7])) for r in rows}
out={}
for k,v in sorted(pairs.items()):
    if len(v)!=2: print("unpaired",k,v); continue
    r=W.stats(D+v['ref']); h=W.stats(D+v['hypo'])
    w=W.wer(r['words'],h['words'])
    out[k]=dict(ref=v['ref'],hypo=v['hypo'],n_r=r['n'],n_h=h['n'],al_r=r['avglen'],al_h=h['avglen'],albug_r=r['avglen_buggy'],albug_h=h['avglen_buggy'],
        lines_r=r['nlines'],blank_r=r['nblank'],lines_h=h['nlines'],blank_h=h['nblank'],v_r=r['vowels'],v_h=h['vowels'],**w)
json.dump(out,open('all_pairs.json','w'),indent=1)
json.dump(paper,open('paper.json','w'),indent=1)
print(len(out),"pairs computed")
# match to paper by WER (4dp)
import itertools
pw={i:p['wer'] for i,p in paper.items()}
matched=0
for k,o in sorted(out.items(), key=lambda x:x[1]['wer']):
    best=min(pw, key=lambda i:abs(pw[i]-o['wer']))
    print(f"{k:12s} wer={o['wer']:.4f} nr={o['n_r']:5d} nh={o['n_h']:5d} | nearest paper #{best} wer={pw[best]:.4f} (n_h={paper[best]['n_h']}, n_r={paper[best]['n_r']}) diff={o['wer']-pw[best]:+.4f}")
