#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd 

cpi  = pd.read_csv("cpi.dat", comment="#", sep='\s+',  names=["Loops", "inside" , "pi" , "error" ,  "time"])
cpi_sorted = cpi.sort_values(by=["Loops"])

print (cpi_sorted)

#plt.title('cpi_mc performance')

# ....

#plt.savefig('cpi_scaling_plot.png')
