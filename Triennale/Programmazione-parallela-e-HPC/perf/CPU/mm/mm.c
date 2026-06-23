/******************************************************************************
* FILE: ser_mm.c
* DESCRIPTION:  
*   Serial Matrix Multiply - C Version
* AUTHOR: Blaise Barney
* LAST REVISED: 04/12/05
******************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>      // clock_gettime
#include <unistd.h>    // optarg

void options(int argc, char * argv[]);
void usage(char * argv[]);

int n=1000;   // dimensione lato matrice quadrata
int verbose=0;   

char hostname[100];

#define BILLION  1000000000L;

struct timespec start, stop;
double tempo;

int main(int argc, char *argv[])
{

options(argc, argv);  /* optarg management */

gethostname(hostname, 100);

int NCB, NRA, NCA;
NCB=n; NRA=n; NCA=n;
float gflop=(float)n*n*n*2/BILLION; 

double *a,*b,*c;

a=(double *)malloc(sizeof(double)*NRA*NCA);
b=(double *)malloc(sizeof(double)*NCA*NCB);
c=(double *)malloc(sizeof(double)*NRA*NCB);

if (verbose) printf("# Starting serial matrix multiple example...\n");
if (verbose) printf("# Using matrix sizes a[%d][%d], b[%d][%d], c[%d][%d]\n",
        NRA,NCA,NCA,NCB,NRA,NCB);

int    i, j, k;                 /* misc */

/* Initialize A, B, and C matrices */
if (verbose) printf("# Initializing matrices...\n");

   for (i=0; i<NRA; i++)
      for (j=0; j<NCA; j++)
          *(a+i*NCA+j)= i+j;
   for (i=0; i<NCA; i++)
      for (j=0; j<NCB; j++)
          *(b+i*NCA+j)= i*j;
   for(i=0;i<NRA;i++)
      for(j=0;j<NCB;j++)
         *(c+i*NCA+j)= 0.0;

/* Perform matrix multiply */
if (verbose) printf("# Performing matrix multiply...\n");

  clock_gettime( CLOCK_REALTIME, &start);

   for(i=0;i<NRA;i++)
      for(j=0;j<NCB;j++)
         for(k=0;k<NCA;k++)
            *(c+i*NCB+j)+= *(a+i*NCA+k) * *(b+k*NCB+j);

  clock_gettime( CLOCK_REALTIME, &stop);

 tempo = (double) ( stop.tv_sec - start.tv_sec )
          + (double) ( stop.tv_nsec - start.tv_nsec )
            / BILLION;

if (verbose) 
{
printf("Here is the result matrix:");
for (i=0; i<NRA; i++) { 
   printf("\n"); 
   for (j=0; j<NCB; j++) 
      printf("%6.2f   ",  *(c+i*NCB+j));
   }
  printf("\n");
}

printf("# N  gflop  tempo(s)  GFLOPs  Hostname  \n");
printf("%d, %.2f,  %.2f,   %.2f,  %s \n", n, gflop, tempo, gflop/tempo, hostname); 
   
if (verbose) printf ("\n#Done.\n");
}


void options(int argc, char * argv[])
{
  int i;
   while ( (i = getopt(argc, argv, "n:vh")) != -1) {
        switch (i)
        {
        case 'n':  n = strtol(optarg, NULL, 10);  break;
        case 'v':  verbose = 1 ; break;
        case 'h':  usage(argv); exit(1);
        case '?':  usage(argv); exit(1);
        default:   usage(argv); exit(1);
        }
    }
}

/***************************************/

void usage(char * argv[])
{
  printf ("\n  [-n <dim_lato_matrice> ] [-v] [-h] \n ");
  return;
}

