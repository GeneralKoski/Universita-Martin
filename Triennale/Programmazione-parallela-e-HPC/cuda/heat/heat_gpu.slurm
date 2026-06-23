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

nvcc -O2  heat_gpu.cu -o heat_gpu

heat_gpu -x 32 -y 32  -c 1024 -r 1024  -s 1000 1> heatmap.out  2> heat_gpu.csv

