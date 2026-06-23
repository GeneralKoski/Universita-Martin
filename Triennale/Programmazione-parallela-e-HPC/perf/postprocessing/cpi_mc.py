#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd 

cpi_mc = pd.read_csv("cpi_mc.csv", comment="#", sep='\s+',  names=["Loops", "inside" , "pi" , "error" ,  "time"])
sorted = cpi_mc.sort_values(by=["Loops"])

print (sorted)

# ESEMPIO:
#plt.title('cpi_mc performance')
#plt.grid()
#plt.xlabel('Loops')
#plt.yscale('log')
#plt.ylabel('error')
#plt.plot(sorted.Loops,sorted.error,'ro-',label='CPI')
#plt.legend(shadow=True)
#plt.savefig('cpi_scaling_plot.png')
