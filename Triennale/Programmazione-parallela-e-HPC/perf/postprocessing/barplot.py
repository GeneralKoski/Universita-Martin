#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd 

df = pd.read_csv("barplot_data.csv",comment="#", sep='\s+')
#print df

df.plot(kind='bar',  x='device');
# https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.DataFrame.plot.html

plt.ylabel('performance')
plt.xticks(rotation=45)
plt.savefig('barplot.png')
