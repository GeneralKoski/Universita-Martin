#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')   # Backend per PNG 
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("mpi_cpi_scaling.dat", names=["par","nt","n","t","t1","t2","e1","e2","host"])
df4 = pd.read_csv("mpi_cpi_scaling-4.dat", names=["par","nt","n","t","t1","t2","e1","e2","host"])

#print(df)

df1=df[df["n"]==1000000000]
df2=df[df["n"]==2000000000]
df4=df[df["n"]==4000000000]

df14=df4[df4["n"]==1000000000]
df24=df4[df4["n"]==2000000000]
df44=df4[df4["n"]==4000000000]


print (df44)

plt.subplot(2,1,1)

plt.title('CPI MPI scaling ')
plt.grid()
plt.xlabel('tasks')
plt.ylabel('time')
plt.yscale('log')
plt.plot(df4.nt,  df4.t, '-o', label="CPI-4Giter-1n")
plt.plot(df44.nt,  df44.t, '-o', label="CPI-4Giter-4n")
plt.legend(shadow=True,loc="best")

plt.subplot(2,1,2)

plt.grid()
plt.xlabel('tasks')
plt.ylabel('speedup')
plt.plot(df4.nt,  df4.t.iloc[0]/df4.t,  '-o', label="CPI-4Giter-1n")
plt.plot(df44.nt,  df44.t.iloc[0]/df44.t,  '-o', label="CPI-4Giter-4n")
plt.plot(range(1,60),range(1,60),'-r', label='Ideal')
plt.legend(shadow=True,loc="best")

plt.savefig('mpi_cpi_scaling-4.png')
