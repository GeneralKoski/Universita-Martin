#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')   # Backend per PNG 
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("mpi_pym_cpi_scaling.dat", names=["par","nt","n","t","t1","t2","e1","e2","host"])

#print(df)

dfM=df[ df["par"]=="MPI" ]
dfP=df[ df["par"]=="PYM" ]

#print (dfM)
#print (dfP)


plt.subplot(2,1,1)

plt.title('CPI MPI scaling ')
plt.grid()
plt.xlabel('tasks')
plt.ylabel('time')
plt.yscale('log')
plt.plot(dfM.nt,  dfM.t, '-o', label="MPI CPI-100Miter")
plt.plot(dfP.nt,  dfP.t, '-o', label="PYM CPI-100Miter")
plt.legend(shadow=True,loc="best")

plt.subplot(2,1,2)

plt.grid()
plt.xlabel('tasks')
plt.ylabel('speedup')
plt.plot(dfM.nt,  dfM.t.iloc[0]/dfM.t,  '-o', label="MPI CPI-100Miter")
plt.plot(dfP.nt,  dfP.t.iloc[0]/dfP.t,  '-o', label="PYM CPI-100Miter")
plt.plot(range(1,30),range(1,30),'-r', label='Ideal')
plt.legend(shadow=True,loc="best")

plt.savefig('mpi_pym_cpi_scaling.png')


