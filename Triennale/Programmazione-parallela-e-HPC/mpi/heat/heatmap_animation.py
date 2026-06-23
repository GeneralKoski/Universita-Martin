import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from numpy import genfromtxt

outfile='heatmap-animation'

if len(sys.argv) == 2:
  outfile=sys.argv[1]

bashCommand="module purge"
print (bashCommand)
os.system(bashCommand)
bashCommand="module load gnu openmpi"
print (bashCommand)
os.system(bashCommand)

for i in xrange(0,15000,1000):
  bashCommand = "mpirun -n 8 mpi_heat -c 512 -r 512 1"+str(i) +" > mpi_heat.out"
  os.system(bashCommand)
  filename=outfile+str(i).rjust(6,'0') +".png"
  a = genfromtxt('mpi_heat.out', delimiter=' ')
  plt.imsave(filename,a, cmap='hot')
  print ("outfile: " + filename)


bashCommand="convert -delay 20 -loop 0 "+ outfile  + "*.png " + outfile + ".gif"
print (bashCommand)
os.system(bashCommand)

bashCommand="rm "+ outfile  + "*.png"
print (bashCommand)
os.system(bashCommand)
