import matplotlib.pyplot as plt

sizes = [4, 5, 6]
backtracking = [0.01, 0.05, 0.2]
brute = [0.5, 5, 999]

plt.plot(sizes, backtracking, marker='o', label="Backtracking")
plt.plot(sizes, brute, marker='o', label="Brute-force")

plt.xlabel("Grid Size")
plt.ylabel("Time (seconds)")
plt.title("Algorithm Comparison")

plt.legend()
plt.grid()

plt.savefig("chart.png")
plt.show()