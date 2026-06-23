#!/bin/bash
     
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu
#SBATCH --job-name="mpi_hello-GNU_compiler"
#SBATCH --output=%x.o%j
##SBATCH --error=%x.e%j  #If error is not specified stderr is redirected to stdout
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4 
     
## Uncomment the following line if you need an amount of memory other than default (512MB)
##SBATCH --mem=2G
     
## Uncomment the following line if your job needs a wall clock time other than default (1 hour) 
## Please note that priority of queued job decreases as requested time increases
##SBATCH --time=0-00:30:00 
     
## Uncomment the following line if you want to use an account other than your default account ( see hpc-show-user-account )
##SBATCH --account=<account> 
     
echo "# SLURM_JOB_NODELIST     : $SLURM_JOB_NODELIST"
echo "# SLURM_CPUS_PER_TASK    : $SLURM_CPUS_PER_TASK"
echo "# SLURM_JOB_CPUS_PER_NODE: $SLURM_JOB_CPUS_PER_NODE"
     
# Gnu compiler
module load gnu openmpi
mpicc mpi_hello.c -o mpi_hello
mpirun mpi_hello
     
# Uncomment the following lines to compile and run using the INTEL compiler
#module load intel intelmpi
#mpicc mpi_mm.c -o mpi_mm_intel
#mpirun  mpi_hello_intel
     
# Uncomment the following lines to compile and run using the PGI compiler
#module load pgi/2018 openmpi/2.1.2/2018 
#mpicc mpi_hello.c -o mpi_hello_pgi
#mpirun --mca mpi_cuda_support 0 mpi_hello_pgi
