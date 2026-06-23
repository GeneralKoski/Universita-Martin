#!/bin/bash

#SBATCH --partition=cpu_guest
#SBATCH --qos=cpu_guest
#SBATCH --output=%x.o%j
#SBATCH --ntasks=4
##SBATCH --nodes=1
##SBATCH --ntasks-per-node=4
#SBATCH --time=0-00:15:00

#genera modulo da 72 bit:
openssl genrsa -out rsa_key.pem 72 2> /dev/null ; openssl rsa -in rsa_key.pem -modulus -noout

Modulus=AD3E75438E7ACB7B9      

module purge
module load gnu openmpi 

# versione parallela senza gestione della terminazione 
mpicc -O2  mpi_factorize_todo.c -o  mpi_factorize_todo  -lcrypto -lm

# il task che trova il numero primo comunica con gli altri task
mpicc -O2  mpi_factorize.c      -o mpi_factorize        -lcrypto -lm

# suddivisione fine-grain dei task
# gstione checkpoint: l'opzione -s consente di iniziare da un blocco definito
mpicc -O2  mpi_factorize_fine.c -o mpi_factorize_fine   -lcrypto -lm

mpirun  mpi_factorize_todo        -m $Modulus -a 8   > mpi_factorize_todo.txt
mpirun mpi_factorize             -m $Modulus -a 8   > mpi_factorize.txt
mpirun mpi_factorize_fine -s 44  -m $Modulus -a 8   > mpi_factorize_fine.txt

cat mpi_factorize_todo.txt mpi_factorize.txt mpi_factorize_fine.txt > "$Modulus".txt

rm mpi_factorize_todo.txt mpi_factorize.txt mpi_factorize_fine.txt
