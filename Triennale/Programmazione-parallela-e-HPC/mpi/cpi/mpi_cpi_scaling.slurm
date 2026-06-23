#!/bin/bash

#SBATCH --output=%x.o%j
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH --ntasks=64
#SBATCH --nodes=1
##SBATCH --ntasks-per-node=4
#SBATCH --time=0-00:10:00
##SBATCH  --exclude=wn20


echo  "#SLURM_JOB_NODELIST      : $SLURM_JOB_NODELIST"
echo  "#SLURM_JOB_CPUS_PER_NODE : $SLURM_JOB_CPUS_PER_NODE"


module load gnu openmpi
#module load intel impi
mpicc -O2  mpi_cpi.c  -o  mpi_cpi -lm

for N in 1000000000 2000000000 4000000000 
do
  for NT in 1 2 4  8 16 32 64 
  do
    mpirun -n $NT mpi_cpi -n $N 
  done
done   > mpi_cpi_scaling.dat

