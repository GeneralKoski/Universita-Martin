#!/bin/bash

#SBATCH --output=%x.o%j
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
##SBATCH  --ntasks=32
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --time=0-00:10:00
##SBATCH  --nodelist=wn21
##SBATCH  --exclude=wn20

echo  "#SLURM_NTASKS            : $SLURM_NTASKS"
echo  "#SLURM_JOB_NODELIST      : $SLURM_JOB_NODELIST"
echo  "#SLURM_JOB_CPUS_PER_NODE : $SLURM_JOB_CPUS_PER_NODE"

#module load intel impi
module load gnu openmpi
mpicc -O2  mpi_cpi.c  -o  mpi_cpi -lm

for N in 1000000000 2000000000 4000000000 
do
  for NT in 1 2 4  8 16 32 
  do
    mpirun  -n $NT mpi_cpi -n $N 
  done
done   > mpi_cpi_scaling-4.dat

