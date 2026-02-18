fib_seq = [1, 1]
max_value = 5000
i = 1 # Python uses 0-based indexing

while (fib_seq[i] + fib_seq[i-1]) < max_value:
    fib_seq.append(fib_seq[i] + fib_seq[i-1])
    i += 1

print(fib_seq)