#!/bin/bash

#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH --output=%x.o%j
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24
#SBATCH --time=0-12:00:00


echo "#SLURM_JOB_NODELIST: $SLURM_JOB_NODELIST"

module purge
module load gnu8

gcc omp_factorize.c -o omp_factorize -fopenmp -lcrypto -lm

#time ./factorize -m F52D204F85FA23653E4B76AD
for numThread in 1 8 16 24
do
	time OMP_NUM_THREADS=$numThread ./omp_factorize -m B43958313D8573329 -a 4 > omp_factorize_$numThread.out   # modulus 68 bit - prime 34 bit (4 addr + 30 block)
done
