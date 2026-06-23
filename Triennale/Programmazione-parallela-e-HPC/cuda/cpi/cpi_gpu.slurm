#!/bin/sh
 
#SBATCH --output=%x.o%j
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:p100:1
#SBATCH --time=0-00:05:00
#SBATCH --mem=12G

#stampa il nome del nodo assegnato e argomenti                 
echo "#SLURM_JOB_NODELIST   : $SLURM_JOB_NODELIST"
echo "#CUDA_VISIBLE_DEVICES : $CUDA_VISIBLE_DEVICES"

module load cuda 

threadsPerBlock=1024
nblocks=1024

nvcc cpi_gpu_global.cu -o cpi_gpu_global 
cpi_gpu_global   -b $nblocks -t $threadsPerBlock

nvcc cpi_gpu_shr.cu -o cpi_gpu_shr
cpi_gpu_shr         -b $nblocks -t $threadsPerBlock

