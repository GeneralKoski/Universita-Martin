#!/bin/sh
 
##SBATCH --partition=gpu_guest
#SBATCH --partition=gpu
#SBATCH --mem=4G
#SBATCH --qos=gpu
#SBATCH --gres=gpu:p100:1
#SBATCH --time=0-00:20:00

#stampa il nome del nodo assegnato e argomenti                 
echo "#SLURM_JOB_NODELIST   : $SLURM_JOB_NODELIST"
echo "#CUDA_VISIBLE_DEVICES : $CUDA_VISIBLE_DEVICES"

module load cuda

nvcc -O2  heat_gpu_shr.cu -o heat_gpu_shr
nvcc -O2  heat_gpu.cu -o heat_gpu

rm heat_gpu_shr_scaling.dat
rm heat_gpu_scaling.dat

for N in 512 1024 2048 4096
do
    ./heat_gpu_shr -r $N -c $N -s 100000 2>> heat_gpu_shr_scaling.dat
    ./heat_gpu -r $N -c $N -s 100000 2>> heat_gpu_scaling.dat
done

