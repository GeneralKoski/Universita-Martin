#!/bin/bash

#SBATCH --output=%x.o%j-P100  # Nome del file per lo strandard output
##SBATCH --error=%x.e%j  # Se non specificato stderr e' rediretto su stdout 
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --nodes=1
#SBATCH --gres=gpu:p100:1
##SBATCH --gres=gpu:a100_80g:1
#SBATCH --time=0-0:02:00
##SBATCH --account=T_2023_HPCPROGPAR

module load gnu/5.4.0   cuda/11.5.2
 
./deviceQuery
