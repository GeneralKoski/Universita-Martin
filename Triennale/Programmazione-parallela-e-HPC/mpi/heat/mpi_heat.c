/*
heat.c

module load intel
icc -O2 heat.c -o heat

heat -h
heat -s 10 -r 16 -c 16 -d
heat -r 4096 -c 4096
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <mpi.h>

#define BILLION  1000000000L;


void options(int argc, char * argv[]) ;
void usage(char * argv[]);
void Jacobi_Iterator_CPU(float * __restrict T, float * __restrict T_new, const int _NX, const int _NY); 
void Init_center(float * __restrict h_T, const int _NX, const int _NY); // center 
void Init_left(float * __restrict h_T, const int _NX, const int _NY);   // left border
void Init_top(float * __restrict h_T, const int _NX, const int _NY);    // top border
void copy_rows(float * __restrict h_T, const int _NX, const int _NY);   // periodic boundary conditions
void copy_cols(float * __restrict h_T, const int _NX, const int _NY);   // periodic boundary conditions
void print_colormap(float * __restrict h_T, int _NY, int _NX);                         // 

int WNX = 24;         // --- Number of discretization points along the x axis
int WNY = 24;         // --- Number of discretization points along the y axis
int MAX_ITER = 1000;  // --- Number of Jacobi iterations
int debug=0;
int NX, NY;

double timeStart, timeStop, totalTime;

  float *h_T_new;
  float *h_T_old;
  float *h_T_temp;
  float *h_T_whole;


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
    
    int iter,i,j;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &MPIrank);
    MPI_Comm_size(MPI_COMM_WORLD, &MPIsize);

    NX = WNX;
    NY = WNY/MPIsize+2;

    prev_rank = (MPIrank-1+MPIsize) % MPIsize;
    next_rank = (MPIrank+1) % MPIsize;


    h_T_new = (float *)calloc(NX * NY, sizeof(float));
    h_T_old = (float *)calloc(NX * NY, sizeof(float));
    //h_T_temp = (float *)calloc(NX * NY, sizeof(float));

    if (MPIrank == 0)
      h_T_whole  = (float *)calloc(WNX * WNY, sizeof(float));

    timeStart = MPI_Wtime();

    for(iter=0; iter<MAX_ITER; iter=iter+1)
    {
      if (MPIrank==0)
      {
          Init_center(h_T_old, NX, NY);
          //Init_left(h_T_old, NX, NY);
          //Init_top(h_T_old, NX, NY);
          //copy_rows(h_T_old, NX, NY);
          copy_cols(h_T_old, NX, NY);
      }

      MPI_Sendrecv( &(h_T_old[NX*(NY-2)]), NX, MPI_FLOAT, next_rank, tag,
        &(h_T_old[NX*0]), NX, MPI_FLOAT, prev_rank, tag, 
        MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      
      MPI_Sendrecv( &(h_T_old[NX*1]), NX, MPI_FLOAT, prev_rank, tag,
        &(h_T_old[NX*(NY-1)]), NX, MPI_FLOAT, next_rank, tag,
        MPI_COMM_WORLD, MPI_STATUS_IGNORE);

      Jacobi_Iterator_CPU(h_T_old, h_T_new, NX, NY);

      h_T_temp = h_T_new;
      h_T_new = h_T_old;
      h_T_old = h_T_temp;
    }

    timeStop = MPI_Wtime();
    totalTime = timeStop-timeStart;

  if(MPIrank==0)
    fprintf (stderr,"%d, %d, %d, %.3f \n", WNX, WNY, MAX_ITER, totalTime);

    MPI_Gather(&(h_T_old[NX]), NX*(NY-2), MPI_FLOAT, h_T_whole, NX*(NY-2), MPI_FLOAT, 0, MPI_COMM_WORLD);

  if (MPIrank==0)
    print_colormap(h_T_whole,WNX,WNY);

  free(h_T_new);
  free(h_T_old);
  //free(h_T_temp);

  MPI_Finalize();
  if (MPIrank == 0)
    free(h_T_whole);


  return 0;
}


/***********************************/
/* JACOBI ITERATION FUNCTION - CPU */
/***********************************/
void Jacobi_Iterator_CPU(float * __restrict T, float * __restrict T_new, const int _NX, const int _NY)
{
int i,j;

        // --- Only update "interior" (not boundary) node points
        for(j=1; j<_NY-1; j++)
            for(i=1; i<_NX-1; i++) {
                float T_E = T[(i+1) + _NX*j];
                float T_W = T[(i-1) + _NX*j];
                float T_N = T[i + _NX*(j+1)];
                float T_S = T[i + _NX*(j-1)];
                T_new[_NX*j + i] = 0.25*(T_E + T_W + T_N + T_S);
            }
}


/********************************/
/* TEMPERATURE INITIALIZATION : */
/* parte centrale della griglia */
/********************************/
void Init_center(float * __restrict h_T, const int _NX, const int _NY)
{
    int i,j;
    int startx=_NX/2-_NX/10;
    int endx=_NX/2+_NX/10;
    int starty=_NY/2-_NY/10;
    int endy=_NY/2+_NY/10;
//    int starty=_NY/4;
//    int endy=_NY-_NY/4;
    for(i=startx; i<endx; i++)
        for(j=starty; j<endy; j++)
              h_T[_NX*j + i] = 1.0;
}


/********************************/
/* TEMPERATURE INITIALIZATION : */
/* bordo sinistro               */
/********************************/
void Init_left(float * __restrict h_T, const int _NX, const int _NY)
{

    int i,j;
    int startx=1;
    int endx=2;
    int starty=0;
    int endy=_NY-1;
    for(i=startx; i<endx; i++)
        for(j=starty; j<endy; j++)
              h_T[_NX*j + i] = 1.0;
}


/********************************/
/* TEMPERATURE INITIALIZATION : */
/* bordo alto                   */
/********************************/
void Init_top(float * __restrict h_T, const int _NX, const int _NY)
{
    int i,j;
    int startx=0;
    int endx=_NX-1;
    for(i=startx; i<endx; i++)
              h_T[_NX + i] = 1.0;
}


/********************************/
/* Periodic boundary conditions */
/* COPY BORDER: COLS            */
/********************************/
void copy_cols (float * __restrict h_T, const int _NX, const int _NY)
{

int i;

// copy cols
  for (i = 1; i < _NY-1; ++i) {
    h_T[_NX*i+0]    = h_T[_NX*i+_NX-2];
    h_T[_NX*i+_NX-1] = h_T[_NX*i+1];
  }
}

/********************************/
/* Periodic boundary conditions */
/* COPY BOREDER: ROWS           */
/********************************/
void copy_rows (float * __restrict h_T, const int _NX, const int _NY)
{

   memcpy(&(h_T[_NX*0])      ,&(h_T[_NX*(_NY-2)]), _NX*sizeof(float) );
   memcpy(&(h_T[_NX*(_NY-1)]) ,&(h_T[_NX*1]),      _NX*sizeof(float) );
}

/******************************************/
/* print color map                        */
/******************************************/

void print_colormap(float * __restrict h_T, int _NY, int _NX)
{
   int i,j;

   for (j=1; j<_NY-1; j++){
        for (i=1; i<_NX-1; i++) {
            printf("%2.2f ",h_T[_NX*j + i]);
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
        case 'c':  WNX       = strtol(optarg, NULL, 10);  break;
        case 'r':  WNY       = strtol(optarg, NULL, 10);  break;
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
