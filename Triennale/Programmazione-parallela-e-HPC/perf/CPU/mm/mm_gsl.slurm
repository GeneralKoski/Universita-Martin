#!/bin/bash

#SBATCH --output=%x.o%j  # Nome del file per lo strandard output
##SBATCH --error=%x.e%j  # Se non specificato stderr e' rediretto su stdout
#SBATCH --partition=cpu_guest        # Nome della partizione, cpu per job pargsleli
#SBATCH --qos=cpu_guest              # 
#SBATCH --nodes=1                    # numero di nodi richiesti
#SBATCH --cpus-per-task=1            # numero di cpu 
##SBATCH --mem=2G                    # massima memoria utilizzata
#SBATCH --time=0-00:10:00            # massimo tempo di calcolo

HOST=$(hostname)
MHZ=$(lscpu | grep "CPU MHz:" | sed 's/CPU MHz://g' | sed 's/ //g' )
GFLOPS=$(echo "scale=2; $MHZ *16 / 1000" | bc)
echo  "# $HOST  - $MHZ MHz -  $GFLOPS GFLOPS (Peak)"

echo -n "# " ; gcc --version | grep gcc
echo 

gcc mm_gsl.c -lgsl 
out=$(a.out)
echo "$out, gcc4"

gcc -O2 mm_gsl.c -lgsl
out=$(a.out)
echo "$out, gcc4-O2"

gcc -O2 mm_gsl.c -lgsl
out=$(a.out -g)
echo "$out, gcc4-O2-GSL"

module load  gcc/13.2.0
echo -n "# "; gcc --version | grep gcc

gcc -O2 mm_gsl.c -lgsl
out=$(a.out)
echo "$out, gcc13-O2"

gcc -O2 mm_gsl.c -lgsl
out=$(a.out -g)
echo "$out, gcc13-O2-GSL"

gcc -O2 mm_gsl.c -march=native -ffast-math -lgsl
out=$(a.out)
echo "$out, gcc13-O2-fast"

module purge
module load intel 
echo -n "# " ; icc -v
echo 

icc -O2 mm_gsl.c -lgsl
out=$(a.out)
echo "$out, icc-O2"

icc -O2 mm_gsl.c -lgsl
out=$(a.out -g)
echo "$out, icc-O2-GSL"

icc -O2  -mavx -axCORE-AVX512  mm_gsl.c -lgsl
out=$(a.out)
echo "$out, icc-O2-AVX"

