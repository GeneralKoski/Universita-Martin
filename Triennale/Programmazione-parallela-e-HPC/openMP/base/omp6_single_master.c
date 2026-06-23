#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>


int main(int argc, char *argv[])
{
 int nt=omp_get_max_threads();
 int tid;
 double t_start;
 double *t_array = (double *) malloc( nt*sizeof(double) ); 

 t_start=omp_get_wtime(); 

 #pragma omp parallel shared(t_array) private(tid) 
  {
    tid=omp_get_thread_num();

   #pragma omp master
    { printf("THR-%d MASTER entra sleep 1 \n", tid); sleep(1);
      printf("THR-%d MASTER esce  \n", tid); }

   t_array[tid]=omp_get_wtime();
    
   #pragma omp critical
   printf("%d dopo master %f\n", tid, t_array[tid] - t_start);

    #pragma omp single
     { printf("THR-%d SINGLE entra sleep 1 \n",tid); sleep(1); 
       printf("THR-%d SINGLE esce \n",tid); }

   t_array[tid]=omp_get_wtime(); 

   #pragma omp critical
   printf("%d dopo single %f\n", tid, t_array[tid] - t_start);

  }
        

}

