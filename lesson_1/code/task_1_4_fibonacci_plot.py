import matplotlib.pyplot as plt
import numpy as np

n = 20
fib_seq = [1, 1]
for i in range(2, n):
    fib_seq.append(fib_seq[i-1] + fib_seq[i-2])

fib_seq_15 = np.array(fib_seq[:15])
plt.figure()
plt.plot(fib_seq_15, '-s')
plt.show()

# Calculate ratio (F_n / F_{n-1})
ratio = fib_seq_15[1:] / fib_seq_15[:-1]
print(ratio)

plt.figure()
plt.plot(ratio, '-s')
plt.show()