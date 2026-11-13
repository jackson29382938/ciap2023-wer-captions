"""Independent MAPSSWE (Gillick & Cox 1989; NIST sclite-style) on word-level alignments."""
import math, jiwer
def per_ref_errors(ref, hyp):
    """errors attributed to each reference position; insertions attributed to the preceding ref slot (slot 0 = before first word)."""
    o = jiwer.process_words(' '.join(ref), ' '.join(hyp))
    n = len(ref); e = [0]*(n+1)   # e[0] insertions before first ref word; e[i+1] belongs to ref word i (+ insertions after it)
    for chunks in o.alignments:
        for c in chunks:
            if c.type == 'equal': continue
            if c.type == 'insert':
                e[c.ref_start_idx] += (c.hyp_end_idx - c.hyp_start_idx)
            else:
                for r in range(c.ref_start_idx, c.ref_end_idx):
                    e[r+1] += 1
                if c.type == 'substitute':
                    extra = (c.hyp_end_idx-c.hyp_start_idx)-(c.ref_end_idx-c.ref_start_idx)
                    if extra>0: e[c.ref_end_idx] += extra
    return e
def mapsswe(ref, hypA, hypB, min_gap=2):
    eA, eB = per_ref_errors(ref, hypA), per_ref_errors(ref, hypB)
    segs=[]; cur=[0,0]; clean_run=0; started=False
    for a,b in zip(eA,eB):
        if a==0 and b==0:
            clean_run+=1
            if started and clean_run>=min_gap:
                segs.append(tuple(cur)); cur=[0,0]; started=False
        else:
            clean_run=0; started=True; cur[0]+=a; cur[1]+=b
    if started: segs.append(tuple(cur))
    z=[a-b for a,b in segs]; n=len(z)
    if n<2: return dict(n_seg=n,W=float('nan'),p=float('nan'),mean=float('nan'))
    mu=sum(z)/n; var=sum((x-mu)**2 for x in z)/(n-1)
    if var==0: return dict(n_seg=n,W=0.0,p=1.0,mean=mu)
    W=mu/math.sqrt(var/n); p=math.erfc(abs(W)/math.sqrt(2))
    return dict(n_seg=n,W=W,p=p,mean=mu,sdz=math.sqrt(var))
