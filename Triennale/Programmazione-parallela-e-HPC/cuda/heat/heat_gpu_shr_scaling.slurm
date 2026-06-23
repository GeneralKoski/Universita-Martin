#!/bin/sh
 
#SBATCH --output=%x.o%j
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:p100:1
#SBATCH --mem=4G
#SBATCH --time=0-00:01:00

#stampa il nome del nodo assegnato e argomenti                 
echo "#SLURM_JOB_NODELIST   : $SLURM_JOB_NODELIST"
echo "#CUDA_VISIBLE_DEVICES : $CUDA_VISIBLE_DEVICES"

module load cuda
nvcc -O2  heat_gpu_shr.cu -o heat_gpu_shr

OUTPUT='heat_gpu_shr_scaling.dat'
echo -n "" >$OUTPUT

for N in 512 1024 2048 4096
do
		./heat_gpu_shr  -c $N -r $N -s 10000 2>>$OUTPUT
done

