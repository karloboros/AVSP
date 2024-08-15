import hashlib
import sys

ulaz = sys.stdin.readlines()
ulaz = [line.strip() for line in ulaz]

n1 = int(ulaz[0])
n2 = int(ulaz[n1+1])
tekstovi = ulaz[1:n1+1]
upiti = ulaz[n1+2:]

def simhash(x):
    sh = [0]*128
    tekst = x.split(" ")
    for t in tekst:
        hash = hashlib.md5(t.encode()).hexdigest()
        hash1 = format(int(hash, 16), 'b').zfill(128)
        for i in range(128):
            if hash1[i] == '1': sh[i] += 1
            else: sh[i] -= 1
    for i in range(128):
        if sh[i] >= 0: sh[i] = 1
        else: sh[i] = 0
    return ''.join(map(str, sh))

def hamming(x, y):
    udaljenost = 0
    for i in range(128):
        if x[i] != y[i]: udaljenost += 1
    return udaljenost

#print(simhash("fakultet elektrotehnike i racunarstva"))

hashevi = []
for tekst in tekstovi:
    hashevi.append(simhash(tekst))

izlaz = []
for upit in upiti:
    upit = upit.split(" ")
    i = int(upit[0])
    k = int(upit[1])
    
    ref = hashevi[i]
    sim = 0

    for j, hash in enumerate(hashevi):
        if i == j: continue
        if (hamming(ref, hash) <= k): 
            sim += 1
    izlaz.append(sim)

for a in izlaz: print(a)
