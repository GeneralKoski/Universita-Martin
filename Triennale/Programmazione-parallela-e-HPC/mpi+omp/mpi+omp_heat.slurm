#!/bin/bash
#SBATCH --output=%x.o%j
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=4
#SBATCH --time=0-00:40:00

module purge
module load gnu openmpi

N=100

mpicc -O2 mpi+omp_heat.c -fopenmp -o mpi+omp_heat
mpirun ./mpi+omp_heat -c $N -r $N 1> /dev/null 2> mpi+omp_heat.dat

