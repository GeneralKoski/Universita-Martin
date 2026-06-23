/*
  mpi_DataMining.c
Tutti i progcessi definiscono lo stesso intero x (ad esempio x=7) e
generano ogni secondo un intero random tra 0 e 100
Chi trova il numero x  invia un messaggio agli altri con il numero trovato e termina.
Tutti gli altri processi ricevono e stampano il valore ricevuto e il mittente, quindi  terminano

Scrivere il programma mpi_DataMining_bcast.c il cui il Task 0 invia a tutti l'intero x

module load intel impi
mpicc mpi_DataMining.c -o mpi_DataMining
mpirun  mpi_DataMining
*/

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <mpi.h>

int main (int argc, char *argv[])
{
 MPI_Status status;
 MPI_Request request;
 int  MPIrank, MPIsize;
 int r, i, x, flag,  received;

 // Inizializzo MPI
 MPI_Init(&argc, &argv);
 MPI_Comm_rank(MPI_COMM_WORLD, &MPIrank);
 MPI_Comm_size(MPI_COMM_WORLD, &MPIsize);

 srand48((unsigned)time(NULL)*MPIrank); // inizializzazione del seme per il generatore di numeri casuali
 flag=0;

 // if (MPIrank==0)  
 x=7; 
 // invio di x da rank 0 a tutti gli altri 


 // attiva la ricezione asincrona non bloccante di x
 MPI_Irecv(&received, 1,MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &request);
 printf ("Task %d/%d MPI_Irecv started \n", MPIrank, MPIsize);

 while(!flag)
 {
  r=drand48()*100;    // intero random tra 0 e 100
  printf ("Task %d/%d - x:%d  r:%d \n", MPIrank, MPIsize, x, r);
  if (r == x) 
    for (i=0; i<MPIsize ;i++) MPI_Send(&r, 1, MPI_INT, i, 666, MPI_COMM_WORLD);  //  Invio a tutti di r
  sleep(1);
  MPI_Test( &request, &flag, &status);
 }

 printf ("Task %d/%d - RECEIVED %d from %d, exiting ...\n", MPIrank, MPIsize, received,  status.MPI_SOURCE); // Quando un PROCESSO riceve il numero "x", verrà stampato il valore ricevuto x e il mittente
 MPI_Finalize(); // Termina il programma MPI

 return 0;
}
