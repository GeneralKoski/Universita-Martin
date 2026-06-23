#!/bin/bash

#SBATCH --output=%x.o%j  # Nome del file per lo strandard output
#SBATCH --partition=cpu_guest        # Nome della partizione
#SBATCH --qos=cpu_guest    
#SBATCH --nodes=1                    # numero di nodi richiesti
#SBATCH --cpus-per-task=32            # numero di cpu 
#SBATCH --time=0-00:15:00            # massimo tempo di calcolo
##SBATCH --account=T_2023_HPCPROGPAR  # account da utilizzare

for NT in 1 2 4 8 16 32
do
    OMP_NUM_THREADS=$NT ./omp_heat -c 2048 -r 2048 1> /dev/null
done 2> omp_heat_scaling2048.dat

for NT in 1 2 4 8 16 32
do
    OMP_NUM_THREADS=$NT ./omp_heat -c 4096 -r 4096 1> /dev/null
done 2> omp_heat_scaling4096.dat
