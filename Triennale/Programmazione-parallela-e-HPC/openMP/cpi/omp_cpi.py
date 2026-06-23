#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd 

df1 = pd.read_csv("omp_cpi_scaling_1mld.csv", comment="#", names=["Inter", "numThreads", "n", "tnp", "time1", "time2", "error1", "error2", "hostname"] )
df2 = pd.read_csv("omp_cpi_scaling_10mld.csv", comment="#", names=["Inter", "numThreads", "n", "tnp", "time1", "time2", "error1", "error2", "hostname"] )

print (df1)
print (df2)

plt.title("omp_cpi")
plt.grid()

plt.xlabel("numThreads")
plt.ylabel("tnp")

plt.plot(df1["numThreads"], df1["tnp"], 'r-o', label="1mld", color="green")
plt.plot(df2["numThreads"], df2["tnp"], 'r-o', label="10mld", color="red")

plt.legend(shadow=True)
plt.savefig('omp_cpi.png')
