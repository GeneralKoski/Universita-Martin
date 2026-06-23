#include <stdio.h>
#include <omp.h>

int main(int argc, char* argv[])
{
 int i,j; 
 int tid; // thread id 

 omp_set_num_threads(5);
        
 #pragma omp parallel  private(i,tid)
 {
   tid=omp_get_thread_num();

//   #pragma omp for schedule(dynamic)
   #pragma omp for schedule(static,1) 
   for(j=0; j<5; j++)
    for(i=0; i<5; i++)
      printf("Esecuzione del thread %d:   j=%d i=%d \n", tid, j, i);

   printf("%d ha finito\n", tid);
 }
return 0;
}

