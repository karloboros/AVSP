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
    x = list(str(x))
    y = list(str(y))
    for i in range(len(x)):
        if x[i] != y[i]: udaljenost += 1
    return udaljenost

def lsh(hashevi, b = 8):
    kandidati = {}
    for i in range(1, b+1):
        pretinci = {}
        for j, hash in enumerate(hashevi):
            val = hash2int(b, i, hash[int((i-1)*(128/b)):int(i*(128/b))])
            tekstovi_u_pretincu = []
            if val in pretinci:
                tekstovi_u_pretincu = pretinci[val]
                for tekst_id in tekstovi_u_pretincu:
                    if j not in kandidati: kandidati[j] = []
                    if int(tekst_id) not in kandidati: kandidati[int(tekst_id)] = []
                    if int(tekst_id) not in kandidati[j]: kandidati[j].append(int(tekst_id))
                    if j not in kandidati[int(tekst_id)]: kandidati[int(tekst_id)].append(j)
            else:
                tekstovi_u_pretincu = []
            tekstovi_u_pretincu.append(j)
            pretinci[val] = tekstovi_u_pretincu
    return kandidati

def hash2int(b, pojas, hash):
    hash1 = list(hash)
    hash1.reverse()
    num = 0
    for i in range(len(hash1)):
        num += int(hash1[i])*2**((128/b)*(pojas-1)+i)
    return(int(num))

#print(simhash("fakultet elektrotehnike i racunarstva"))

hashevi = []
for tekst in tekstovi:
    hashevi.append(simhash(tekst))

kandidati = lsh(hashevi)

izlaz = []
for upit in upiti:
    upit = upit.split(" ")
    i = int(upit[0])
    k = int(upit[1])
    
    ref = hashevi[i]
    sim = 0
    if i not in kandidati:
        izlaz.append(0)
        continue
    for kandidat in kandidati[i]:
        if (hamming(ref, hashevi[kandidat]) <= k): sim += 1
    izlaz.append(sim)

for a in izlaz: print(a)
