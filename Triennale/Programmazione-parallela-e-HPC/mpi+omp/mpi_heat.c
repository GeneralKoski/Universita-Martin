/*
mpi_heat.c

module load gnu openmpi
mpicc -O2 mpi_heat.c -o mpi_heat

mpirun mpi_heat -h
mpirun mpi_heat -r 24 -c 24 -s 4
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <mpi.h>

int WNX = 256;         // --- Number of discretization points along the x axis
int WNY = 256;         // --- Number of discretization points along the y axis
int MAX_ITER = 1000;  // --- Number of Jacobi iterations
int NX,NY;

#include "mpi_heat.h"


// variabili globali per MPI
int mpi_rank=0, mpi_size=0;
int prev_rank=0, next_rank=0;
int tag = 999;
MPI_Status status;
char hostname[MPI_MAX_PROCESSOR_NAME]; int namelen;

float *h_T_new;
float *h_T_old;
float *h_T_temp;
float *h_T_whole;

/********/
/* MAIN */
/********/
int main(int argc, char **argv)
{

   int iter,i,j;

   double t1, t2;

   options(argc, argv);         /* optarg management */

   MPI_Init(&argc, &argv);
   MPI_Comm_rank(MPI_COMM_WORLD, &mpi_rank);
   MPI_Comm_size(MPI_COMM_WORLD, &mpi_size);
   MPI_Get_processor_name(hostname,&namelen);

// scomposizione di dominio:
// dividiamo le righe tra i rank MPI
   prev_rank = (mpi_rank-1+mpi_size) % mpi_size;
   next_rank = (mpi_rank+1) % mpi_size;
   NX      =  WNX;                       // Local NX: numero colonne per rank
   NY      =  WNY/mpi_size+2;            // Local NY: numero righe   per rank

// stampa tutti i dati della simulazione
   fprintf (stderr,"# WNX:%d, WNY:%d, MAX_ITER:%d, MPI_RANK:%d, MPI_SIZE:%d, NX:%d, NY:%d, %s \n", WNX, WNY, MAX_ITER, mpi_rank, mpi_size, NX, NY, hostname);

   h_T_new          = (float *)calloc(NX * NY, sizeof(float));
   h_T_old          = (float *)calloc(NX * NY, sizeof(float));
   if (mpi_rank == 0)  h_T_whole  = (float *)calloc(WNX * WNY, sizeof(float));


  t1=MPI_Wtime();

  for(iter=0; iter<MAX_ITER; iter=iter+1)
    {

//    Init_center(h_T_old,  NX, NY);
//    Init_left(h_T_old,    NX, NY);
  if (mpi_rank==0)   Init_top(h_T_old,     NX, NY);
//    copy_rows(h_T_old, NX, NY);
//    copy_cols(h_T_old, NX, NY);

// scambio delle righe di bordo
    // downward
   MPI_Sendrecv( &(h_T_old[NX*(NY-2)]), NX, MPI_FLOAT, next_rank, tag, //send
               &(h_T_old[NX*0]),      NX, MPI_FLOAT, prev_rank, tag, //recv
               MPI_COMM_WORLD, MPI_STATUS_IGNORE);
   // upward
   MPI_Sendrecv( &(h_T_old[NX*1]),    NX, MPI_FLOAT, prev_rank, tag, //send
               &(h_T_old[NX*(NY-1)]), NX, MPI_FLOAT, next_rank, tag, //recv
               MPI_COMM_WORLD, MPI_STATUS_IGNORE);

    Jacobi_Iterator_CPU(h_T_old, h_T_new, NX, NY);

    h_T_temp=h_T_new;
    h_T_new=h_T_old;
    h_T_old=h_T_temp;

    }

  t2=MPI_Wtime();

  if(mpi_rank == 0)   fprintf(stderr,"MPI, %d, %d, %d, %d,  %f\n", mpi_size,  WNX, WNY, MAX_ITER, t2-t1);

  MPI_Gather(&(h_T_old[NX]), NX*(NY-2), MPI_FLOAT, h_T_whole,  NX*(NY-2), MPI_FLOAT,  0,  MPI_COMM_WORLD);

  if (mpi_rank == 0) print_colormap(h_T_whole,WNX,WNY);

   free(h_T_new);
   free(h_T_old);
   if (mpi_rank == 0 ) free(h_T_whole);

   MPI_Finalize();

   return 0;
}


