import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd 

df2048 = pd.read_csv("heat_scaling2048.csv", comment="#", names=["nProcess","nx","ny","iter","time"]) 
print (df2048)
df4096 = pd.read_csv("heat_scaling4096.csv", comment="#", names=["nProcess","nx","ny","iter","time"]) 
print (df4096)
df8192 = pd.read_csv("heat_scaling8192.csv", comment="#", names=["nProcess","nx","ny","iter","time"]) 
print (df8192)

plt.subplot(2,1,1)

plt.title('HEAT Scaling MPI')
plt.grid()
plt.xlabel('nProcess')
#plt.yscale('log')
plt.ylabel('time')
plt.plot(df2048["nProcess"],df2048["time"],'r-o',label='2048', color="blue")
plt.plot(df4096["nProcess"],df4096["time"],'r-o',label='4096', color="red")
plt.plot(df8192["nProcess"],df8192["time"],'r-o',label='8192', color="green")
plt.legend(shadow=True)

plt.subplot(2,1,2)

plt.grid()
plt.xlabel('nProcess')
plt.ylabel('speedup')
plt.plot(df2048["nProcess"],  df2048["time"].iloc[0]/df2048["time"],  '-o',label='2048', color="blue")
plt.plot(df4096["nProcess"],  df4096["time"].iloc[0]/df4096["time"],  '-o',label='4096', color="red")
plt.plot(df8192["nProcess"],  df8192["time"].iloc[0]/df8192["time"],  '-o',label='8192', color="green")
plt.plot(range(1,30),range(1,30),'-r', label='Ideal')
plt.legend(shadow=True,loc="best")

plt.savefig('heat_scaling.png')
