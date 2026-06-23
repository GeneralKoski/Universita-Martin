#!/bin/bash

#SBATCH --output=%x.o%j  # Nome del file per lo strandard output
#SBATCH --partition=cpu_guest        # Nome della partizione
#SBATCH --qos=cpu_guest    
#SBATCH --nodes=1                    # numero di nodi richiesti
#SBATCH --cpus-per-task=1            # numero di cpu 
#SBATCH --time=0-00:10:00            # massimo tempo di calcolo
##SBATCH --account=T_2023_HPCPROGPAR  # account da utilizzare



echo "nx,ny,iter,time" > heat_scaling.csv

for N  in   512 758 1024 2048
do
./heat -c $N  -r $N -s 1000  > /dev/null # il file heatmap non viene creato
done   2>> heat_scaling.csv

