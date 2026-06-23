/*
  mpi_DataMining.c
  Tutti i processi definiscono lo stesso intero x (ad esempio x=7) e
  generano ogni secondo un intero random tra 0 e 100.
  Chi trova il numero x invia un messaggio agli altri con il numero trovato e termina.
  Tutti gli altri processi ricevono e stampano il valore ricevuto e il mittente, quindi terminano.

  Scrivere il programma mpi_DataMining_bcast.c in cui il Task 0 invia a tutti l'intero x

  module load intel impi
  mpicc mpi_DataMining.c -o mpi_DataMining
  mpirun mpi_DataMining
*/

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <mpi.h>

int main (int argc, char *argv[])
{
 MPI_Status status; // Struttura per verificare lo STATO di una COMUNICAZIONE MPI
 MPI_Request request; // Struttura per gestire RICHIESTE non bloccanti in MPI
 int MPIrank, MPIsize;
 int r, i, x, flag, received;

 // Inizializzo MPI
 MPI_Init(&argc, &argv);
 MPI_Comm_rank(MPI_COMM_WORLD, &MPIrank); // Ottiene il RANK del PROCESSO CORRENTE
 MPI_Comm_size(MPI_COMM_WORLD, &MPIsize); // Ottiene il NUMERO TOTALE di PROCESSI

 srand48((unsigned)time(NULL) * MPIrank); // Inizializzazione del seme per il generatore di numeri casuali
 flag = 0; // Serve per verificare la RICEZIONE di un MESSAGGIO

 if (MPIrank == 0)  
     x = 7; // Solo il task 0 inizializza x

 // Task 0 invia x a tutti gli altri processi
 MPI_Bcast(&x, 1, MPI_INT, 0, MPI_COMM_WORLD); // Broadcast del valore di x da parte del task 0 a tutti gli altri processi

 // Attiva la ricezione asincrona non bloccante di x
 MPI_Irecv(&received, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &request); // Inizializza una RICEZIONE NON BLOCCANTE (MPI_Irecv) per ricevere un intero (received) da qualsiasi sorgente (MPI_ANY_SOURCE) e con qualsiasi tag (MPI_ANY_TAG)
 printf ("Task %d/%d MPI_Irecv started \n", MPIrank, MPIsize); // Stampa un MESSAGGIO Che indica che la RICEZIONE ASINCRONA è iniziata

 while (!flag)
 {
     r = drand48() * 100;    // Intero random tra 0 e 100
     printf ("Task %d/%d - x:%d  r:%d \n", MPIrank, MPIsize, x, r); // Stampa il rank del processo, il numero totale di processi, 'x' e il numero casuale generato 'r'
     if (r == x) // Se r è uguale ad x, ovvero il valore inviato dal Task 0
         for (i = 0; i < MPIsize; i++) 
             MPI_Send(&r, 1, MPI_INT, i, 666, MPI_COMM_WORLD);  // Invio r a tutti i PROCESSI
     sleep(1);
     MPI_Test(&request, &flag, &status); // Verifico se è arrivato un messaggio e aggiorna 'flag' e 'status' di conseguenza
 }

 printf ("Task %d/%d - RECEIVED %d from %d, exiting ...\n", MPIrank, MPIsize, received, status.MPI_SOURCE); // Quando un processo riceve il numero "x", stampa il valore ricevuto e il mittente
 MPI_Finalize(); // Termina il programma MPI

 return 0;
}
