#!/bin/bash

#SBATCH --output=%x.o%j   # Nome del file per lo strandard output
##SBATCH --error=%x.e%j  # Se non specificato stderr e' rediretto su stdout
#SBATCH --partition=cpu_guest       # Nome della partizione, cpu per job paralleli
#SBATCH --qos=cpu_guest              # 
#SBATCH --nodes=1                    # numero di nodi richiesti
#SBATCH --cpus-per-task=1            # numero di cpu 
##SBATCH --mem=2G                    # massima memoria utilizzata
#SBATCH --time=0-00:02:00            # massimo tempo di calcolo
#SBATCH --account=T_2023_HPCPROGPAR  # Account da usare
##Notare che il doppio ##  disabilita la direttiva.

hostname

lscpu

numactl --hardware

