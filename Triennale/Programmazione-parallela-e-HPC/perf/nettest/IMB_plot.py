#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd 

imb1 = pd.read_csv("IMB-MPI1.shm.dat",comment="#", sep='\s+',  names=["bytes", "repetitions","time","MBps"] )
imb2 = pd.read_csv("IMB-MPI1.opa.dat",comment="#", sep='\s+',  names=["bytes", "repetitions","time","MBps"] )

plt.title('IMB throughput')
plt.grid()
plt.xlabel('bytes')
plt.xscale('log')
plt.ylabel('MBps')
plt.plot(imb1.bytes,imb1.MBps,'ro-',label='SHM')
plt.plot(imb2.bytes,imb2.MBps,'bo-',label='OPA')
plt.legend()
plt.savefig('IMB_thr.png')

plt.clf()

plt.title('IMB Latency')
plt.xscale('log')
plt.xlabel('bytes')
plt.ylabel('time(us)')
plt.plot(imb1.bytes,imb1.time,'ro-',label='SHM')
plt.plot(imb2.bytes,imb2.time,'bo-',label='OPA')
plt.legend()
plt.axis([1,100,0,5])

plt.savefig('IMB_lat.png')
#plt.show()
