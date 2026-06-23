import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from numpy import genfromtxt

a = genfromtxt('mpi_heatmap.out', delimiter=' ')
plt.imsave('mpi_heatmap.png',a, cmap='hot')
