import sys
import math

def add_bit(bit, buckets, current_time):
    current_time += 1
    if bit:
        buckets.append((1, current_time))
    return buckets, current_time

def merge_buckets(buckets):
    i = 0
    while i < len(buckets) - 2:
        if buckets[i][0] == buckets[i + 1][0] == buckets[i + 2][0]:
            new_bucket = (buckets[i][0] * 2, buckets[i + 1][1])
            buckets.pop(i)
            buckets[i] = new_bucket
            i = max(0, i-2)
        else:
            i += 1
    return buckets

def remove_buckets(buckets, current_time, N):
    while buckets and buckets[0][1] <= current_time - N:
        buckets.pop(0)
    return buckets

def query(k, buckets, current_time):
    result = 0
    threshold = current_time - k
    last = 0

    for size, timestamp in reversed(buckets):
        if timestamp > threshold:
            result += size
            last = size
        else:
            break

    result = result - last + math.floor(last / 2)
    return result

"""
ulaz = []
with open('lab6_ulaz4.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        ulaz.append(line)
"""
ulaz = sys.stdin.read().strip().split('\n')

N = int(ulaz[0])
buckets = []
current_time = -1

for line in ulaz[1:]:
    if line.startswith('q'):
        k = int(line.split()[1])
        print(query(k, buckets, current_time))
    else:
        for bit in line:
            buckets, current_time = add_bit(int(bit), buckets, current_time)
            buckets = remove_buckets(buckets, current_time, N)
            if bit: buckets = merge_buckets(buckets)
