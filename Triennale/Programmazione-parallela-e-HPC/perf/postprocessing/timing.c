/*
 * https://linux.die.net/man/3/clock_gettime
 * This program calculates the time required to
 * execute the program specified as its first argument.
 * The time is printed in seconds, on standard out.
 * CLOCK_REALTIME              Wall-Clock time
 * CLOCK_PROCESS_CPUTIME_ID    per-process timer from the CPU
 * gcc timing.c -o timing -O2
 */


#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
 
#define BILLION  1000000000L;

int main( int argc, char **argv )
  {
    struct timespec start_wall, stop_wall, start_cpu, stop_cpu;
    double wall_time, cpu_time;
 
   clock_gettime( CLOCK_REALTIME ,          &start_wall) ;
   clock_gettime( CLOCK_PROCESS_CPUTIME_ID , &start_cpu) ;

   sleep (3); 

   int i;
    double j;
   for (i = 0; i < 1000000000; i++) { j+=i*0.001; }
   printf( "j=%.4lf \n", j);
 
   clock_gettime( CLOCK_REALTIME           , &stop_wall ) ;
   clock_gettime( CLOCK_PROCESS_CPUTIME_ID , &stop_cpu ) ;

   wall_time = (double) ( stop_wall.tv_sec - start_wall.tv_sec )
            + (double) ( stop_wall.tv_nsec - start_wall.tv_nsec )
            / BILLION;

   cpu_time = (double) ( stop_cpu.tv_sec - start_cpu.tv_sec )
            + (double) ( stop_cpu.tv_nsec - start_cpu.tv_nsec )
            / BILLION;


    printf( "Wall-clock: %.4lf, CPU-time: %.4lf \n", wall_time, cpu_time);

    return( EXIT_SUCCESS );
  }
