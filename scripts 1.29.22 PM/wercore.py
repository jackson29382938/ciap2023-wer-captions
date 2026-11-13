"""Re-implementation of the manuscript's normalization (refinement-pywer.py) with a correct word-length statistic."""
import re, string, os
import jiwer

TIME = re.compile(r'\b\d{1,2}:\d{2}(:\d{2})?\s?(?:[APap][Mm])?\b')
NUM = {str(i): w for i, w in enumerate(
 "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split())}
tens = {20:'twenty',30:'thirty',40:'forty',50:'fifty',60:'sixty',70:'seventy',80:'eighty',90:'ninety'}
ones = "one two three four five six seven eight nine".split()
for t,w in tens.items():
    NUM[str(t)] = w
    for k,o in enumerate(ones,1): NUM[str(t+k)] = f"{w}-{o}"
NUM['100'] = 'one hundred'
def _num(m): return NUM.get(m.group(0), m.group(0))
TRANS = str.maketrans('', '', '\n' + string.punctuation)

def norm_line(line, phrase="sir tifi dinsane "):
    line = line.replace(phrase, '')
    line = TIME.sub('', line)
    line = re.sub('Sir Tifi Dinsane', '', line)
    line = re.sub(r'\b\d{1,3}\b', _num, line)
    line = line.translate(TRANS)
    line = re.sub(r' {2,3}', ' ', line)
    return line.lower()

def read_words(path):
    words, line_avgs, vowels = [], [], 0
    with open(path, 'r', errors='ignore') as f:
        for line in f:
            l = norm_line(line)
            w = l.split()
            tl = sum(len(x) for x in w)
            line_avgs.append(tl/len(w) if w else 0.0)   # what the original script did (blank lines -> 0)
            vowels += sum(1 for c in l if c in 'aeiouAEIOU')
            words += w
    return words, line_avgs, vowels

def stats(path):
    w, la, v = read_words(path)
    n = len(w)
    return dict(n=n, avglen=(sum(map(len,w))/n if n else float('nan')),
                avglen_buggy=(sum(la)/len(la) if la else float('nan')),
                nlines=len(la), nblank=sum(1 for x in la if x==0.0), vowels=v, words=w)

def wer(ref, hyp):
    o = jiwer.process_words(' '.join(ref), ' '.join(hyp))
    return dict(wer=o.wer, S=o.substitutions, D=o.deletions, I=o.insertions)
