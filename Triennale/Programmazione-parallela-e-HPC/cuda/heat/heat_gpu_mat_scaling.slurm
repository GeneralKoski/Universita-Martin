#!/bin/sh
 
##SBATCH --partition=gpu_guest
#SBATCH --partition=gpu
#SBATCH --nodes=1 
#SBATCH --mem=4G
#SBATCH --qos=gpu
#SBATCH --gres=gpu:p100:1
#SBATCH --time=0-00:10:00

module load cuda
nvcc -O2  heat_gpu.cu -o heat_gpu

rm heat_gpu_mat_scaling.dat

for N in 512 1024 2048 4096
do
    ./heat_gpu  -c $N -r $N -s 10000 2>> heat_gpu_mat_scaling.dat
done

