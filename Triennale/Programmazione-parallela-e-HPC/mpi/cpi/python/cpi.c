#include <stdio.h>
#include <math.h>
#include <unistd.h>    //optarg
#include <time.h>      //gettime
#include <stdlib.h>

void options(int argc, char * argv[]) ;
void usage(char * argv[]);
double f1 (long int);
double f2 (long int);

long int n=1000000000;    // intervalli
int s=0;                 // tempo sleep 
double h; 
char hostname[100];

#define BILLION  1000000000L;

 struct timespec ta,tb,tc,td;
 double tnp, tp1, tp2; 
 double sum1, sum2;
 double pi1, pi2;

/********************************************/

int main( int argc, char *argv[])
{
   clock_gettime( CLOCK_REALTIME  , &ta); ////////////////////////////////

    double  PI = 3.14159265358979323846264338327950288 ;

    gethostname(hostname, 100); 

    options(argc, argv);  /* optarg management */ 

    h = 1.0 / (double) n;

    sleep (s);  // Simulazione codice non paralellizzabile

   clock_gettime( CLOCK_REALTIME  , &tb); ////////////////////////////////

    sum1= f1(n); 

   clock_gettime( CLOCK_REALTIME , &tc); ////////////////////////////////

    sum2= f2(n); 

   clock_gettime( CLOCK_REALTIME , &td); ////////////////////////////////

   pi1 = 4 * h * sum1;
   pi2 = 4 * h * sum2;

   tnp = (double) ( tb.tv_sec  - ta.tv_sec )
       + (double) ( tb.tv_nsec - ta.tv_nsec )/ BILLION;

   tp1 = (double) ( tc.tv_sec  - tb.tv_sec )
       + (double) ( tc.tv_nsec - tb.tv_nsec )/ BILLION;

   tp2 = (double) ( td.tv_sec  - tc.tv_sec )
       + (double) ( td.tv_nsec - tc.tv_nsec )/ BILLION;

    fprintf(stderr,"#Inter       error1        error2       tnp       tp        time1       time2       hostname \n");
    fprintf(stdout,"C,  %ld,  %.8e, %.8e,  %.5f, %.5f, %.5f, %s \n",
                n,  fabs(pi1-PI), fabs(pi2-PI),  tp1+tp2, tp1, tp2, hostname);

    return 0;
}

double f1 (long int n )
 { 
    long int i; 
    double x, sum=0.0; 
    for (i = 1; i <= n; i++)
     {
       x = h * ((double)i - 0.5);
       sum += sqrt(1-x*x) ;
     }
     return sum; 
 }

double f2 (long int n )
 {
    long int i; 
    double x, sum=0.0;
    for (i = 1; i <= n; i++)
     {
       x = h * ((double)i - 0.5);
       sum += (1.0 / (1.0 + x*x));
     }
     return sum;
 }

/************************************************/

void options(int argc, char * argv[]) 
{
  int i;
   while ( (i = getopt(argc, argv, "n:s:h")) != -1) {
        switch (i) 
        {
        case 'n':  n  = strtol(optarg, NULL, 10);  break;
        case 's':  s  = strtol(optarg, NULL, 10);  break;
        case 'h':  usage(argv); exit(1);
        case '?':  usage(argv); exit(1);
        default:   usage(argv); exit(1);
        }
    }
}

/***************************************/

void usage(char * argv[])
{
  printf ("\n%s [-n intervals] [-s sleep] [-h]",argv[0]); 
  printf ("\n"); 
}

