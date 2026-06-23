#!/bin/bash

#SBATCH --output=%x.o%j
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --time=0-00:10:00
##SBATCH --exclude=wn20

gcc -O2 -fopenmp omp_cpi.c -o omp_cpi -lm

for NT in {1..8}
do
	OMP_NUM_THREADS=$NT ./omp_cpi -n 1000000000
done > omp_cpi_scaling_1mld.csv

for NT in {1..8}
do
	OMP_NUM_THREADS=$NT ./omp_cpi -n 10000000000
done > omp_cpi_scaling_10mld.csv
