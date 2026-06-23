#!/bin/sh

#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --mem=4G
#SBATCH --qos=gpu
#SBATCH --gres=gpu:p100:1
#SBATCH --time=0-00:10:00

module load cuda

nvcc -O2 heat_gpu.cu -o heat_gpu

for BLOCKSIZE in 4 8 16 32
do
    output_file="heat_gpu_block_${BLOCKSIZE}_scaling.dat"
    rm -f $output_file  # Usa -f per non mostrare errori se il file non esiste

    for N in 512 1024 2048 4096 8192
    do
        ./heat_gpu -x $BLOCKSIZE -y $BLOCKSIZE -r $N -c $N -s 10000 2>> $output_file
    done
done

