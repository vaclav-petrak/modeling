import numpy as np

n = 20
fib_seq = [1, 1]

for i in range(2, n):
    fib_seq.append(fib_seq[i-1] + fib_seq[i-2])

print(fib_seq)