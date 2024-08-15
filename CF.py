import copy
import sys
import math
from decimal import Decimal, ROUND_HALF_UP

ulaz = sys.stdin.readlines()
ulaz = [line.strip() for line in ulaz]

prvi = ulaz[0].split(" ")
n = int(prvi[0])
m = int(prvi[1])
x = []
for i in range(1, n+1):
    x.append([])
    temp = ulaz[i].split(" ")
    for j in range(m):
        x[i-1].append(temp[j])
q = ulaz[n+1]
upiti = ulaz[n+2:]

def remove_x(x):
    n = len(x)
    m = len(x[0])
    for i in range(n):
        for j in range(m):
            if(x[i][j]=="X"): x[i][j] = "0"
            x[i][j] = int(x[i][j])
    return x

def pearson(x, t):
    n = len(x)
    m = len(x[0])

    x1 = copy.deepcopy(x)
    if t:
        for i in range(m):
            grades = 0
            sum = 0.0
            for j in range(n):
                if x[j][i] > 0:
                    grades +=1
                    sum += x[j][i]
            if grades == 0: average = 0
            else: average = 1.0*sum/grades
            for j in range(n):
                if x[j][i] > 0:
                    x1[j][i] -= average
    elif not t:    
        for i in range(n):
            grades = 0
            sum = 0.0
            for j in range(m):
                if x[i][j] > 0:
                    grades +=1
                    sum += x[i][j]
            if grades == 0: average = 0
            else: average = 1.0*sum/grades
            for j in range(m):
                if x[i][j] > 0:
                    x1[i][j] -= average
    return x1

def cosine(x, i, j, t):
    sim = []
    if t:
        original = []
        for l in range(len(x)): original.append(x[l][j])
        nazivnik_original = 0.0
        for l in range(len(original)):
            nazivnik_original += original[l]*original[l]
        for l in range(len(x[0])):
            brojnik = 0.0
            nazivnik = 0.0
            for k in range(len(x)):
                brojnik += original[k] * x[k][l]
                nazivnik += x[k][l] * x[k][l]
            if nazivnik != 0:
                sim_item = brojnik/(math.sqrt(nazivnik)*math.sqrt(nazivnik_original))
            else: sim_item = -1
            sim.append(sim_item)
    elif not t:
        original = x[i]
        nazivnik_original = 0.0
        for l in range(len(original)):
            nazivnik_original += original[l]*original[l]
        for l in range(len(x)):
            brojnik = 0.0
            nazivnik = 0.0
            for k in range(len(x[l])):
                brojnik += original[k] * x[l][k]
                nazivnik += x[l][k] * x[l][k]
            if nazivnik != 0:
                sim_item = brojnik/(math.sqrt(nazivnik)*math.sqrt(nazivnik_original))
            else: sim_item = -1
            sim.append(sim_item)
            
    return sim

def find_largest(s, k):
    najveci = []
    pozicije = []
    for j in range(k):
        maximum = 0.0
        max_index = -1

        for i, num in enumerate(s):
            if num > maximum and i not in pozicije:
                maximum = num
                max_index = i
        if max_index != -1 and maximum > 0:
            najveci.append(maximum)
            pozicije.append(max_index)

    pozicije.pop(0)
    return pozicije

def itemitem(x, i, j, t, k):
    x1 = remove_x(x)
    x1 = pearson(x1, t)
    s = cosine(x1, i, j, t)
    positions = find_largest(s, len(s))
    brojnik = 0.0
    nazivnik = 0.0
    k1 = 0
    for p in positions:
        if x[p][j] != 0:
            brojnik += s[p] * x[p][j]
            nazivnik += s[p]
            k1 += 1
        if k1 == k:
            break
    result = brojnik/nazivnik
    return result

def useruser(x, i, j, t, k):
    x1 = remove_x(x)
    x1 = pearson(x1, t)
    s = cosine(x1, i, j, t)
    positions = find_largest(s, len(s))
    brojnik = 0.0
    nazivnik = 0.0
    k1 = 0
    for p in positions:
        if x[i][p] != 0:
            brojnik += s[p] * x[i][p]
            nazivnik += s[p]
            k1 += 1
        if k1 == k:
            break
    result = brojnik/nazivnik
    return result

izlaz = []
for upit in upiti:
    novi = upit.split(" ")
    i = int(novi[0])-1 # red
    j = int(novi[1])-1 # stupac
    t = int(novi[2]) # 0-itemitem, 1-useruser
    k = int(novi[3]) # maksimalni kardinalni broj skupa sličnih stavki/korisnika koje sustav preporuke razmatra prilikom računanja vrijednosti preporuka.

    element = x[i][j]
    if t == 0:
        izlaz.append(itemitem(x, i, j, t, k))
    elif t == 1:
        izlaz.append(useruser(x, i, j, t, k))

for a in izlaz:
    print(Decimal(Decimal(a).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)))
