import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from numpy import genfromtxt

a = genfromtxt('heatmap.out', delimiter=' ')
plt.imsave('heatmap.png',a, cmap='hot')
