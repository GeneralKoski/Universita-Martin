 //  gcc cpi_mc.c -o cpi_mc

#include <stdio.h>
#include <stdlib.h>    // drand48() 
#include <unistd.h>    // optarg
#include <sys/time.h>  // gettimeofday
#include <sys/types.h>
#include <time.h>
#include <math.h>

void options(int argc, char * argv[]) ;
void usage(char * argv[]);


double       PI = 3.14159265358979323846264338327950288 ;

int n=10000000;           // Throws number
int inside=0;
char hostname[100];
double t1, t2, dt12;
struct timeval tempo;


main(int argc, char *argv[])
{
  int i;
  double x, y, pi;
  srand48((unsigned)time(NULL)); // init seed

  options(argc, argv);  /* optarg management */ 

  printf("# n=%d  \n",  n );

 gettimeofday(&tempo,0);  t1=tempo.tv_sec+(tempo.tv_usec/1000000.0); // start timer

  for (i=0; i<n; i++)  {
    x = drand48();
    y = drand48();
    if ( x*x + y*y < 1 ) ++inside;
  }

 gettimeofday(&tempo,0); t2=tempo.tv_sec+(tempo.tv_usec/1000000.0); // stop timer

  dt12=t2-t1; 
  pi = inside/(double)i*4.0;
  printf("#Loops  inside    pi        error          walltime \n");
  printf("%d %d  %.10f  %.10e %.4f \n",n,inside,pi,fabs(PI-pi),dt12);
  return 0; 
}


void options(int argc, char * argv[]) 
{
  int i;
   while ( (i = getopt(argc, argv, "n:p:h")) != -1) {
        switch (i) 
        {
        case 'n':  n = strtol(optarg, NULL, 10);  break;
        case 'h':  usage(argv); exit(1);
        case '?':  usage(argv); exit(1);
        default:   usage(argv); exit(1);
        }
    }
}

/***************************************/

void usage(char * argv[])
{
  printf ("\n%s [-n throws]  [-h]",argv[0]); 
  printf ("\n"); 
}

