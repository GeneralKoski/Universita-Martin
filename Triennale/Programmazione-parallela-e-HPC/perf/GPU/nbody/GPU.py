#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd 

df = pd.read_csv("GPU.csv", comment="#", names=["Hostname", "GFLOPs"] )

print df

df.plot(kind='bar',  x='Hostname', y='GFLOPs', legend='true');
# https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.DataFrame.plot.html


plt.legend()
plt.ylabel('GFLOPs')
plt.savefig('GPU.png')


