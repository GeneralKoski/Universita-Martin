/*
Nel programma mpi_reduction.c tutti gli N task inviano il proprio rank con MPI_Send() al task 0.
Il task 0 itera  N volte MPI_recv()  per ricevere tutti messaggi, sommarli e stampare il risultato.

Scirvere il programma mpi_reduction_collective.c che raggiunge lo stesso risultato ma utilizzando la 
funzione collettiva MPI_Reduce()
*/

#include <stdio.h>
#include "mpi.h"

int main (int argc, char *argv[]) {
 MPI_Status status;
 int i, mpi_rank, mpi_size, reduction=0, received;


 MPI_Init(&argc, &argv);
 MPI_Comm_rank(MPI_COMM_WORLD, &mpi_rank);
 MPI_Comm_size(MPI_COMM_WORLD, &mpi_size);

MPI_Reduce(&mpi_rank, &reduction, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD); 

if (mpi_rank==0) printf ("mpi_size: %d, reduction: %d \n", mpi_size,  reduction); 

 MPI_Finalize();
 return 0;
}
