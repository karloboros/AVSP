import itertools
import sys
import math

ulaz = sys.stdin.readlines()
ulaz = [line.strip() for line in ulaz]

"""
ulaz = []
with open('ulaz.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        ulaz.append(line)
    f.close()
"""

def PCY(ulaz):
    # ucitavanje
    N = int(ulaz[0]) # broj kosara
    s = float(ulaz[1]) # prag podrske

    prag = math.floor(s * N)
    b = int(ulaz[2]) # broj pretinaca na raspolaganju, ako skup podataka sadrzi k razlicitih predmeta, par predmeta i, j sazima se u pretinac formulom: h = ((i*k)+j) %b
    buckets = []
    for i in range(N):
        buckets.append(ulaz[3+i].split(" ")) # predmeti unutar kosare odvojeni su razmakom, svaki je zapisan kao cijeli broj gdje je k broj razlicitih predmeta
    izlaz = []
    
    # prvi prolaz
    items = {}
    for bucket in buckets:
        for item in bucket:
            if item not in items: items[item] = 1
            else: items[item] += 1
    m = 0
    for item, count in items.items():
        if count >= prag: m += 1
    izlaz.append(int(m*(m-1)/2))
    
    # drugi prolaz - sazimanje
    compartments = {}
    pairs = {}
    for bucket in buckets:
        for c in itertools.combinations(bucket, 2):
            item1 = c[0]
            item2 = c[1]
            if (item1, item2) not in pairs: pairs[(item1, item2)] = 0
            pairs[(item1, item2)] += 1
            if items[item1] >= prag and items[item2] >= prag:
                k = ((int(item1) * len(items)) + int(item2)) % b
                if k not in compartments: compartments[k] = 0
                compartments[k] += 1

    # treci prolaz - brojanje parova
    for bucket in buckets:
        for c in itertools.combinations(bucket, 2):
            item1 = c[0]
            item2 = c[1]
            if items[item1] >= prag and items[item2] >= prag:
                k = ((int(item1) * len(items)) + int(item2)) % b
                if compartments[k] >= prag:
                    pairs[(item1, item2)] += 1
    
    list = []
    for item, count in pairs.items():
        if count>prag:
            list.append(int(count/2))
    list.sort()
    list.reverse()
    izlaz.append(len(list))
    for l in list:
        izlaz.append(l)

    return izlaz

"""
izlaz:
A - ukupan broj kandidata cestih parova koje bi brojao algoritam A-priori. Ako je algoritam u prvom prolazu odredio da je m predmeta cesto, onda taj broj iznosi: m*(m-1)/2
P - ukupan broj parova koje prebrojava algoritam pcy, radi se samo o parovima koji se sazimaju u cesti pretinac
X1 - silazno sortirani brojevi ponavljanja cestih parova, navodi se samo ukupan broj ponavljanja za svaki par
X2
...
Xn
"""

izlaz = PCY(ulaz)

for i in izlaz:
    print(i)
