#!/bin/bash
 
#SBATCH --partition=cpu
#SBATCH --qos=cpu
#SBATCH --job-name=omp_hello-GNU_compiler
#SBATCH --output=%x.o%j
 
##SBATCH --error=%x.e%j  #If error is not specified stderr is redirected to stdout
#SBATCH --nodes=1
#SBATCH --cpus-per-task=28
 
## Uncomment the following line if you need an amount of memory other than default (512MB)
##SBATCH --mem=2G
 
## Uncomment the following line if your job needs a wall clock time other than default (1 hour) 
## Please note that priority of queued job decreases as requested time increases
#SBATCH --time=0-00:30:00 
 
## Uncomment the following line if you want to use an account other than your default account (see hpc-show-user-account)
##SBATCH --account=<account> 
 
##SBATCH --exclusive  # uncomment to require a whole node with at least 28 cores 
 
echo "#SLURM_JOB_NODELIST: $SLURM_JOB_NODELIST"
# Comment out the following line in case of exclusive request 
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
echo "#OMP_NUM_THREADS   : $OMP_NUM_THREADS"
 
# Compile and run with the GNU compiler. Default gcc version is 4.8.5. 
# Load the gnu module if you want to use a newer version of the GNU compiler. 
module load gnu 
gcc -fopenmp omp_hello.c -o omp_hello
./omp_hello
 
# Uncomment the following lines to compile and run with the INTEL compiler
#module load intel
#icpc -qopenmp omp_hello.c -o omp_hello_intel
#./omp_hello_intel
 
# Uncomment the following lines to compile and run with the PGI compiler
#module load pgi 
#pgc++ -mp omp_hello.c -o omp_hello_pgi
#/omp_hello_pgi
