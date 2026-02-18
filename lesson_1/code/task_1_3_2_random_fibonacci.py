import random

def random_fibonacci(n):
    fib_seq = [1, 1]
    for i in range(2, n):
        fib_seq.append(fib_seq[i-1] + fib_seq[i-2])
    
    fib_seq = fib_seq[:n]
    return random.choice(fib_seq)

print(random_fibonacci(10))