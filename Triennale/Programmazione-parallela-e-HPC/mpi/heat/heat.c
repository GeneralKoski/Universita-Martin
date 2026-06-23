/*
heat.c

module load intel
icc -O2 heat.c -o heat

heat -h
heat -s 10 -r 16 -c 16 -d
heat -r 4096 -c 4096
*/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <mpi.h>

#define BILLION  1000000000L;


void options(int argc, char * argv[]) ;
void usage(char * argv[]);
void Jacobi_Iterator_CPU(float * __restrict T, float * __restrict T_new, const int NX, const int NY); 
void Init_center(float * __restrict h_T, const int NX, const int NY); // center 
void Init_left(float * __restrict h_T, const int NX, const int NY);   // left border
void Init_top(float * __restrict h_T, const int NX, const int NY);    // top border
void copy_rows(float * __restrict h_T, const int NX, const int NY);   // periodic boundary conditions
void copy_cols(float * __restrict h_T, const int NX, const int NY);   // periodic boundary conditions
void print_colormap(float * __restrict h_T);                          // 

int WNX = 512;         // --- Number of discretization points along the x axis
int WNY = 512;         // --- Number of discretization points along the y axis
int MAX_ITER = 1000;  // --- Number of Jacobi iterations
int debug=0;
int NX, NY;

 double timeStart, timeStop, totalTime;


/********/
/* MAIN */
/********/
int main(int argc, char **argv)
{

    options(argc, argv);         /* optarg management */

    MPI_Status status;
    MPI_Request request;
    int  MPIrank, MPIsize;
    int prev_rank=0, next_rank=0;
    int tag = 999;
    int r, i, x, flag,  received;

    float *h_T_new;
    float *h_T_old;
    float *h_T_temp;
    float *h_T_whole;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &MPIrank);
    MPI_Comm_size(MPI_COMM_WORLD, &MPIsize);

    NY = WNY/MPIsize+2;
    NX = WNX;

    prev_rank = (MPIrank-1+MPIsize) % MPIsize;
    next_rank = (MPIrank+1) % MPIsize;


    h_T_new = (float *)calloc(NX * NY, sizeof(float));
    h_T_old = (float *)calloc(NX * NY, sizeof(float));
    h_T_temp = (float *)calloc(NX * NY, sizeof(float));

    if (MPIrank == 0)
      h_T_whole  = (float *)calloc(WNX * WNY, sizeof(float));

    timeStart = MPI_Wtime();
    int iter,i,j;

    for(iter=0; iter<MAX_ITER; iter=iter+1)
    {
      h_T_temp = h_T_new;  // SWAP
      h_T_new = h_T_old;
      h_T_old = h_T_temp;

      if (MPIrank==0)
      {
        Init_center(h_T_old,  NX, NY);
        //    Init_left(h_T_old,    NX, NY);
        //    Init_top(h_T_old,     NX, NY);
        //    copy_rows(h_T_old, NX, NY);
        copy_cols(h_T_old, NX, NY);
      }

      MPI_Sendrecv( &(h_T_old[NX*(NY-2)]), NX, MPI_FLOAT, next_rank, tag, //send
        &(h_T_old[NX*0]), NX, MPI_FLOAT, prev_rank, tag, //recv
        MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      // upward
      MPI_Sendrecv( &(h_T_old[NX*1]), NX, MPI_FLOAT, prev_rank, tag, //send
        &(h_T_old[NX*(NY-1)]), NX, MPI_FLOAT, next_rank, tag, //recv
        MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        Jacobi_Iterator_CPU(h_T_old, h_T_new, NX, NY);

      h_T_temp = h_T_new;
      h_T_new = h_T_old;
      h_T_old = h_T_temp;
      
      if (debug)
        system("clear"); print_colormap(h_T_old); sleep(1);
    }

    timeStart = MPI_Wtime();

    totalTime = timeStop-timeStart;

    MPI_Gather(&(h_T_old[NX]), NX*(NY-2), MPI_FLOAT, h_T_whole, NX*(NY-2), MPI_FLOAT, 0, MPI_COMM_WORLD);


  if(MPIrank==0)
    fprintf (stderr,"%d, %d, %d, %.3f \n", NX, NY, MAX_ITER, time);

  if (!debug)
    print_colormap(h_T_old);

  free(h_T_new);
  free(h_T_old);
  free(h_T_temp);

  MPI_Finalize();

  if (MPIrank != 0 )
    return 0;
  
  free(h_T_whole);


  return 0;
}


/***********************************/
/* JACOBI ITERATION FUNCTION - CPU */
/***********************************/
void Jacobi_Iterator_CPU(float * __restrict T, float * __restrict T_new, const int NX, const int NY)
{
int i,j;

        // --- Only update "interior" (not boundary) node points
        for(j=1; j<NY-1; j++)
            for(i=1; i<NX-1; i++) {
                float T_E = T[(i+1) + NX*j];
                float T_W = T[(i-1) + NX*j];
                float T_N = T[i + NX*(j+1)];
                float T_S = T[i + NX*(j-1)];
                T_new[NX*j + i] = 0.25*(T_E + T_W + T_N + T_S);
            }
}


/********************************/
/* TEMPERATURE INITIALIZATION : */
/* parte centrale della griglia */
/********************************/
void Init_center(float * __restrict h_T, const int NX, const int NY)
{
    int i,j;
    int startx=NX/2-NX/10;
    int endx=NX/2+NX/10;
    int starty=NY/2-NY/10;
    int endy=NY/2+NY/10;
//    int starty=NY/4;
//    int endy=NY-NY/4;
    for(i=startx; i<endx; i++)
        for(j=starty; j<endy; j++)
              h_T[NX*j + i] = 1.0;
}


/********************************/
/* TEMPERATURE INITIALIZATION : */
/* bordo sinistro               */
/********************************/
void Init_left(float * __restrict h_T, const int NX, const int NY)
{

    int i,j;
    int startx=1;
    int endx=2;
    int starty=0;
    int endy=NY-1;
    for(i=startx; i<endx; i++)
        for(j=starty; j<endy; j++)
              h_T[NX*j + i] = 1.0;
}


/********************************/
/* TEMPERATURE INITIALIZATION : */
/* bordo alto                   */
/********************************/
void Init_top(float * __restrict h_T, const int NX, const int NY)
{
    int i,j;
    int startx=0;
    int endx=NX-1;
    for(i=startx; i<endx; i++)
              h_T[NX + i] = 1.0;
}


/********************************/
/* Periodic boundary conditions */
/* COPY BORDER: COLS            */
/********************************/
void copy_cols (float * __restrict h_T, const int NX, const int NY)
{

int i;

// copy cols
  for (i = 1; i < NY-1; ++i) {
    h_T[NX*i+0]    = h_T[NX*i+NX-2];
    h_T[NX*i+NX-1] = h_T[NX*i+1];
  }
}

/********************************/
/* Periodic boundary conditions */
/* COPY BOREDER: ROWS           */
/********************************/
void copy_rows (float * __restrict h_T, const int NX, const int NY)
{

   memcpy(&(h_T[NX*0])      ,&(h_T[NX*(NY-2)]), NX*sizeof(float) );
   memcpy(&(h_T[NX*(NY-1)]) ,&(h_T[NX*1]),      NX*sizeof(float) );
}

/******************************************/
/* print color map                        */
/******************************************/

void print_colormap(float * __restrict h_T)
{
   int i,j;

   for (j=1; j<NY-1; j++){
        for (i=1; i<NX-1; i++) {
            printf("%2.2f ",h_T[NX*j + i]);
        }
        printf("\n");
        }
}

/******************************************/
/* options management                     */
/******************************************/
void options(int argc, char * argv[]) {

  int i;
   while ( (i = getopt(argc, argv, "c:r:s:hd")) != -1) {
        switch (i) {
        case 'c':  NX       = strtol(optarg, NULL, 10);  break;
        case 'r':  NY       = strtol(optarg, NULL, 10);  break;
        case 's':  MAX_ITER = strtol(optarg, NULL, 10);  break;
        case 'd':  debug=1; break;
        case 'h':  usage(argv); exit(1);
        case '?':  usage(argv); exit(1);
        default:   usage(argv); exit(1);
        }
    }
}

/******************************************/
/* print help                             */
/******************************************/
void usage(char * argv[])  {

  printf ("\n%s [-c ncols] [-r nrows] [-s nsteps] [-d] [-h]",argv[0]);
  printf ("\n");

}
