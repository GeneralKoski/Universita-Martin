#!/bin/bash

#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH --output=%x.o%j

#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-12:00:00


echo "#SLURM_JOB_NODELIST: $SLURM_JOB_NODELIST"

module load gnu8
gcc factorize.c -o factorize -lcrypto  -lm

#time ./factorize -m F52D204F85FA23653E4B76AD
 time ./factorize -m B81915BC0A2222F4B  -a 4    # modulus 68 bit - prime 34 bit (4 addr + 30 block)
