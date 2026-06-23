#!/bin/sh

#SBATCH --output=%x.o%j
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:p100:1
#SBATCH --time=0-00:02:00

# Print the name of the assigned node and arguments
echo "#SLURM_JOB_NODELIST   : $SLURM_JOB_NODELIST"
echo "#CUDA_VISIBLE_DEVICES : $CUDA_VISIBLE_DEVICES"

module purge
module load cuda

nvcc cuda_printf.cu -o cuda_printf && ./cuda_printf > cuda_printf.dat
nvcc sumArray.cu -o sumArray && ./sumArray > sumArray.dat
nvcc matMul.cu -o matMul && ./matMul > matMul.dat
nvcc variabili.cu -o variabili && ./variabili > variabili.dat
nvcc managed.cu -o managed && ./managed > managed.dat
nvcc race_condition.cu -o race_condition && ./race_condition > race_condition.dat
nvcc sezione_critica.cu -o sezione_critica && ./sezione_critica > sezione_critica.dat
nvcc global_sync.cu -o global_sync && ./global_sync > global_sync.dat
