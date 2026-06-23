#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd 

df = pd.read_csv("mm_gsl.csv",comment="#", names=["N", "gflop", "tempo" ,"GFLOPs", "Hostname", "opt"] )

print df

df.plot(kind='bar',  x='opt', y='GFLOPs', legend='true');
# https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.DataFrame.plot.html


plt.legend()
plt.ylabel('GFLOPs')
plt.savefig('mm_gsl.png')


