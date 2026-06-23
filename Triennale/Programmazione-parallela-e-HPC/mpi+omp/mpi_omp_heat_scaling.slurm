#!/bin/bash
#SBATCH --output=%x.o%j
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --time=0-00:15:00

module purge
module load gnu openmpi
#module load intel impi

gcc -O2 heat.c -o heat
gcc -O2 omp_heat.c -fopenmp -o omp_heat
mpicc -O2 mpi_heat.c -o mpi_heat
mpicc -O2 mpi+omp_heat.c -fopenmp -o mpi+omp_heat

rm -f heat_scaling.dat omp_heat_scaling.dat mpi_heat_scaling.dat mpi+omp_heat_scaling.dat

N=4096

for NT in 1 2 4 8
do
 OMP_NUM_THREADS=$NT ./omp_heat -c $N -r $N 1> /dev/null 2>> omp_heat_scaling.dat
 mpirun -np $NT ./mpi_heat -c $N -r $N 1> /dev/null 2>> mpi_heat_scaling.dat
 OMP_NUM_THREADS=$NT mpirun -pernode ./mpi+omp_heat -c $N -r $N 1> /dev/null 2>> mpi+omp_heat_scaling.dat
done

./heat -c $N -r $N 1> /dev/null 2> heat_scaling.dat
