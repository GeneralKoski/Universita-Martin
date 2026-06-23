#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')   # Backend per PNG 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("cpi_scaling.dat", names=["mem", "intervals", "nblock", "threadxblock", "pi", "error", "wtime", "ktime"])

#print(df)

dfG=df[ df["mem"]=="CUDA_G"]
dfS=df[ df["mem"]=="CUDA_S"]

print(dfG)
print(dfS)

plt.subplot(2,1,1)

plt.title('CPI CUDA scaling')
plt.grid()
plt.xlabel('blocks')
plt.ylabel('wTime')
plt.yscale('log')
plt.plot(dfG.nblock, dfG.wtime, '-o', label="CUDA-GLOBAL MEMORY")
plt.plot(dfS.nblock, dfS.wtime, '-o', label="CUDA-SHARED MEMORY")
plt.legend(shadow=True,loc="best")

plt.subplot(2,1,2)

plt.grid()
plt.xlabel('blocks')
plt.ylabel('speedup')

wtime_G_nblock_1 = dfG.loc[dfG['nblock'] == 1, 'wtime'].iloc[0] if not dfG[dfG['nblock'] == 1].empty else None
wtime_S_nblock_1 = dfS.loc[dfS['nblock'] == 1, 'wtime'].iloc[0] if not dfS[dfS['nblock'] == 1].empty else None

speedup_G = wtime_G_nblock_1 / dfG['wtime']
speedup_S = wtime_S_nblock_1 / dfS['wtime']

print("Speedup for CUDA-GLOBAL MEMORY (speedup_G):")
print(speedup_G)
print("Speedup for CUDA-SHARED MEMORY (speedup_S):")
print(speedup_S)

plt.yscale('log')
plt.plot(dfG['nblock'], speedup_G, '-o', label="CUDA-GLOBAL MEMORY")
plt.plot(dfS['nblock'], speedup_S, '-o', label="CUDA-SHARED MEMORY")
plt.legend(shadow=True, loc="best")

plt.savefig('cpi_scaling.png')

