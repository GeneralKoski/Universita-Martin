#!/bin/bash

#SBATCH --output=%x.o%j
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH  --ntasks=32
##SBATCH --nodes=1
##SBATCH --cpus-per-task=64
#SBATCH --time=0-00:30:00
#SBATCH --exclude=wn20


echo  "#SLURM_JOB_NODELIST      : $SLURM_JOB_NODELIST"
echo  "#SLURM_JOB_CPUS_PER_NODE : $SLURM_JOB_CPUS_PER_NODE"


#module load intel impi
module load gnu openmpi
mpicc -O2  mpi_cpi.c  -o  mpi_cpi -lm

#for N in 100000000 200000000 400000000 
for N in 100000000
do
  for NT in 1 2 4 8 16 32 
  do
    mpirun -n $NT mpi_cpi -n $N 
    python3 pym_cpi.py -t $NT -i $N
  done
done   > mpi_pym_cpi_scaling.dat

