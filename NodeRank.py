import sys
from decimal import Decimal, ROUND_HALF_UP

"""
ulaz = []
with open('ulaz.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        ulaz.append(line)
"""
ulaz = sys.stdin.readlines()
ulaz = [line.strip() for line in ulaz]

n, beta = ulaz[0].split(" ")
n = int(n)
beta = float(beta)

rank = [1.0 / n] * n

graph = {}
for i in range(n):
    bridovi = ulaz[i + 1].split(" ")
    graph[i] = [int(brid) for brid in bridovi]

broj_upita = int(ulaz[n + 1])
upiti = []
for u in ulaz[n+2:]:
    s = u.split(" ")
    upiti.append((int(s[0]), int(s[1])))

iteracije = []
iteracije.append(rank)
for t in range(1, 101):
    new_rank = [(1 - beta) / n] * n
    for i in range(n):
        susjedi = graph[i]
        di = len(susjedi)
        for susjed in susjedi:
            new_rank[susjed] += beta * iteracije[t-1][i] / di
    iteracije.append(new_rank)

izlaz=[]
for cvor, iter in upiti:
    izlaz.append(iteracije[iter][cvor])

for i in izlaz:
    print(Decimal(Decimal(i).quantize(Decimal('.0000000001'), rounding=ROUND_HALF_UP)))