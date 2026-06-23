// gcc reduction.c -o reduction -fopenmp

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

main(int argc, char *argv[])
{
  int i,n,  inside=0;
  double x,y;

 int tid, nt;  

if (argc>1) n=atoi(argv[1]); else  n = 100;

 nt=omp_get_max_threads();

#pragma omp parallel  private(tid,x,y)
{
  tid=omp_get_thread_num( );
  srand48((unsigned)time(NULL)*tid); // inizializzazione del seme

#pragma omp for  reduction(+:inside)
  for (i=0; i<n; i++) 
  {
    x = drand48();
    y = drand48();
    if ( x*x + y*y < 1 ) ++inside;
//    printf("thr: %d  i:%d,  inside: %d\n", tid, i, inside); 
  }
 }

 printf("INSIDE: %d   PI: %.5e  NT: %d\n",  inside,  inside/(double)n*4.0, nt );

 return 0;
}
