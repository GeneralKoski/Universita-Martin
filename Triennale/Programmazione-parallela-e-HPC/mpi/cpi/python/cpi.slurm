#!/bin/bash

#SBATCH --output=%x.o%j
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH  --ntasks=1
#SBATCH --nodes=1
##SBATCH --cpus-per-task=64
#SBATCH --time=0-00:10:00

#module purge
#module load intel 

gcc -O2  cpi.c  -o  cpi -lm

#  100 milioni
for  N in 100000000 
do
    cpi -n $N 
    python3 cpi.py -i $N
done   >  cpi.dat

