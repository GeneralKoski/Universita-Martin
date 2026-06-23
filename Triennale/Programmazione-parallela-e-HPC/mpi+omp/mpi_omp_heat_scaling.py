#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg') # backend per png
import matplotlib.pyplot as plt
import pandas as pd


df_heat     = pd.read_csv("heat_scaling.dat", comment="#",  names=["r","c","iter", "time_j", "time_t"])
df_omp     = pd.read_csv("omp_heat_scaling.dat" ,comment="#",   names=["PAR", "thr", "r", "c","iter", "time_t", "time_j"])
df_mpi     = pd.read_csv("mpi_heat_scaling.dat" ,comment="#",  names=["PAR","task","r", "c","iter", "time_t"])
df_mpi_omp     = pd.read_csv("mpi+omp_heat_scaling.dat" ,comment="#",  names=["PAR","task","thr","r", "c","iter", "time_t"])

plt.subplot(2, 1, 1)
plt.title('Heat scaling - 4096x4096')
plt.grid()
plt.ylabel('time')
plt.xlabel('task x thread')
plt.plot(df_omp.thr,df_omp.time_t,'-o', label='openMP')
plt.plot(df_mpi.task,df_mpi.time_t,'-o', label='MPI')
plt.plot((df_mpi_omp.task*df_mpi_omp.thr),df_mpi_omp.time_t,'-o', label='MPI+openMP')
plt.plot(1,df_heat.time_t,'-o', label='serial')
plt.legend(shadow=True,loc="best")

print("\n")

plt.subplot(2, 1, 2)
plt.grid()
plt.xlabel('tasks x threads')
plt.ylabel('Speedup')
plt.plot(df_omp.thr, df_heat.time_t[0]/df_omp.time_t,'-o', label='openMP')
plt.plot(df_mpi.task,df_heat.time_t[0]/df_mpi.time_t,'-o', label='MPI')
plt.plot(df_mpi_omp.task*df_mpi_omp.thr,df_heat.time_t[0]/df_mpi_omp.time_t,'-o', label='MPI+openMP')
plt.plot(range(1,10),range(1,10),'-r', label='Ideal')
plt.legend(shadow=True,loc="best")

plt.savefig('heat_mpi_omp_scaling.png')
