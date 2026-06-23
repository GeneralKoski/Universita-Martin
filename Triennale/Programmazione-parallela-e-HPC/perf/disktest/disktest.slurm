#!/bin/bash
 
#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
##SBATCH --nodelist=wn18
#SBATCH --output=%x.o%j 
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
##SBATCH --mem=2G
#SBATCH --time=0-00:05:00 
 
echo "#SLURM_JOB_NODELIST: $SLURM_JOB_NODELIST"

DISKTEST=~/HPC2324/perf/disktest/disktest.sh

echo "####################################"
echo "# HOME perf"
cd $HOME
pwd
$DISKTEST

echo "####################################"
echo "# SCRATCH perf"
cd $SCRATCH
pwd
$DISKTEST

echo "####################################"
echo "# ARCHIVE perf"
cd $ARCHIVE
pwd
$DISKTEST

echo "####################################"


