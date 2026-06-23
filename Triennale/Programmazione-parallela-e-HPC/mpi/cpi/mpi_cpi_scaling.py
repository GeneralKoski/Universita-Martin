#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')   # Backend per PNG 
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("mpi_cpi_scaling.dat", names=["par","nt","n","t","t1","t2","e1","e2","host"])

#print(df)

df1=df[df["n"]==1000000000]
df2=df[df["n"]==2000000000]
df4=df[df["n"]==4000000000]

print (df4)

plt.subplot(2,1,1)

plt.title('CPI MPI scaling ')
plt.grid()
plt.xlabel('tasks')
plt.ylabel('time')
plt.yscale('log')
plt.plot(df1.nt,  df1.t, '-o', label="CPI-1Giter-1n")
plt.plot(df2.nt,  df2.t, '-o', label="CPI-2Giter-1n")
plt.plot(df4.nt,  df4.t, '-o', label="CPI-4Giter-1n")
plt.legend(shadow=True,loc="best")

plt.subplot(2,1,2)

plt.grid()
plt.xlabel('tasks')
plt.ylabel('speedup')
plt.plot(df1.nt,  df1.t.iloc[0]/df4.t,  '-o', label="CPI-1Giter-1n")
plt.plot(df2.nt,  df2.t.iloc[0]/df4.t,  '-o', label="CPI-2Giter-1n")
plt.plot(df4.nt,  df4.t.iloc[0]/df4.t,  '-o', label="CPI-4Giter-1n")
plt.plot(range(1,60),range(1,60),'-r', label='Ideal')
plt.legend(shadow=True,loc="best")

plt.savefig('mpi_cpi_scaling.png')


