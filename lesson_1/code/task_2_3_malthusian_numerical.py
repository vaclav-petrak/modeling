import matplotlib.pyplot as plt

P0, r = 2.50, 0.027
t_start, t_end, t_diff = 0, 70, 1

t_num = [t_start]
P_num = [P0]

# Numerical calculation loop
for i in range(int(t_end/t_diff)):
    P_new = P_num[i] + r * P_num[i] * t_diff
    t_new = t_num[i] + t_diff
    P_num.append(P_new)
    t_num.append(t_new)

plt.plot(t_num, P_num, color="red")
plt.xlabel("Time (years)")
plt.ylabel("Population (millions)")
plt.ylim(0, 20)
plt.show()