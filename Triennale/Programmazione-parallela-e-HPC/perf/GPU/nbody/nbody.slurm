#!/bin/bash

#SBATCH --output=%x.o%j-p100  # Nome del file per lo strandard output
##SBATCH --error=%x.e%j       # Se non specificato stderr e' rediretto su stdout 
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --nodes=1
#SBATCH --gres=gpu:a100_40g:4
#SBATCH --time=0-00:10:00
##SBATCH --mem=3G
##SBATCH --account=T_2023_HPCPROGPAR  
 
module load gnu/5.4.0   cuda/11.5.2
 
echo "#SLURM_JOB_NODELIST   : $SLURM_JOB_NODELIST"
echo "#CUDA_VISIBLE_DEVICES : $CUDA_VISIBLE_DEVICES"

./nbody  -benchmark -fp64 -numbodies=1024000 -numdevices=1
