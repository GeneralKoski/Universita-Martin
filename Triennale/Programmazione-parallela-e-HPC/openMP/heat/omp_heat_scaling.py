#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd

df1 = pd.read_csv("omp_heat_scaling2048.dat", names=["OMP", "numThreads", "dim1", "dim2", "op", "time"] )
df2 = pd.read_csv("omp_heat_scaling4096.dat", names=["OMP", "numThreads", "dim1", "dim2", "op", "time"] )

print(df1)
print(df2)

# Grafico 1
plt.subplot(2, 1, 1)

plt.title('HEAT Scaling OMP')
plt.grid()

plt.xlabel('Number of Threads')
plt.ylabel('Time: (seconds)')

plt.plot(df1["numThreads"], df1["time"], 'r-o', label="2048", color="blue")
plt.plot(df2["numThreads"], df2["time"], 'r-o', label="4096", color="red")

plt.legend(shadow=True, loc="best")

# Grafico 2
plt.subplot(2, 1, 2)
plt.title('HEAT OMP SpeedUp')
plt.grid()

plt.xlabel('Number of Threads')
plt.ylabel('Speedup')

plt.plot(df1["numThreads"], df1["time"].iloc[0]/df1["time"], 'r-o', label="2048", color="blue")
plt.plot(df2["numThreads"], df2["time"].iloc[0]/df2["time"], 'r-o', label="4096", color="red")
plt.plot(range(1, 32), range(1, 32), 'r', label="ideal")

plt.legend(shadow=True, loc="best")
plt.tight_layout()
plt.savefig('omp_heat_scaling.png')
