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

module purge
module load cuda 

rm -f cpi_scaling.dat

nvcc cpi_gpu_global.cu -o cpi_gpu_global
nvcc cpi_gpu_shr.cu -o cpi_gpu_shr

threadsPerBlock=1024

./cpi_gpu_global -b 1 -t 1 2>> cpi_scaling.dat
for nblocks in 1024 2048 4096 8192
do
 ./cpi_gpu_global -b $nblocks -t $threadsPerBlock 2>> cpi_scaling.dat
done

./cpi_gpu_shr -b 1 -t 1 2>> cpi_scaling.dat
for nblocks in 1024 2048 4096 8192
do
  ./cpi_gpu_shr -b $nblocks -t $threadsPerBlock 2>> cpi_scaling.dat
done