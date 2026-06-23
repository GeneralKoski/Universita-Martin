#!/bin/bash

#SBATCH --output=%x.o%j  # Nome del file per lo strandard output
#SBATCH --partition=cpu_guest        # Nome della partizione
#SBATCH --qos=cpu_guest    
#SBATCH --nodes=10                    # numero di nodi richiesti
#SBATCH --cpus-per-task=2            # numero di cpu 
#SBATCH --time=0-00:10:00            # massimo tempo di calcolo
##SBATCH --account=T_2023_HPCPROGPAR  # account da utilizzare


echo "#SLURM_JOB_NODELIST : $SLURM_JOB_NODELIST"
echo "#SLURM_JOB_CPUS_PER_NODE : $SLURM_JOB_CPUS_PER_NODE"

module purge

module load gnu openmpi
mpicc -O2 mpi_heat.c -o mpi_heat

./mpi_heat >  mpi_heatmap.out


