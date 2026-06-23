#!/usr/bin/env python2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd 

df = pd.read_csv("disktest.csv",comment="#", sep='\s+')

df.plot(kind='bar',  x='device');

plt.title ('Storage test')

plt.ylabel('performance (MB/s)')

plt.savefig ('disktest.png')
