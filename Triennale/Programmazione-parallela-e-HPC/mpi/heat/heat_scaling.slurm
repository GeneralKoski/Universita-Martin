#!/bin/bash
#SBATCH --output=%x.o%j
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH --ntasks=32
#SBATCH --nodes=1
##SBATCH --ntasks-per-node=4
#SBATCH --time=0-00:15:00
##SBATCH --exclude=wn20


echo "#SLURM_JOB_NODELIST : $SLURM_JOB_NODELIST"
echo "#SLURM_JOB_CPUS_PER_NODE : $SLURM_JOB_CPUS_PER_NODE"

export OMPI_MCA_btl=^openib #solve openfabric error

module purge
module load gnu openmpi
module load intel impi


mpicc -O2 mpi_heat.c -o mpi_heat

echo "nx,ny,iter,time" > heat_scaling.csv

for N in 2048 4096 8192
do
    for NT in 1 2 4 8 16 32
    do
        mpirun -n $NT mpi_heat -c $N -r $N 1> /dev/null
    done
done 2> mpi_heat_scaling.dat
