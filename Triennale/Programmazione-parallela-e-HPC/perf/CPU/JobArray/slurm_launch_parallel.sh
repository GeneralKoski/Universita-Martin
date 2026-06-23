#!/bin/sh
#SBATCH --partition=vrt
#SBATCH --qos=vrt
#SBATCH --array=1-10:1

## Charge resources to account
##SBATCH --account=<account>
##SBATCH --mem=4G

N=$((${SLURM_ARRAY_TASK_ID}*1000000))
CMD="./cpi_mc -n $N"
echo "# $CMD"
eval $CMD
