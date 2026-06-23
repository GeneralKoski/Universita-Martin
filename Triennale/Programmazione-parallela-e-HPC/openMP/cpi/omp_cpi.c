// GNU Profiling    https://users.cs.duke.edu/~ola/courses/programming/gprof.html
// gcc cpi.c -pg  -o cpi-pg -lm
// ./cpi-pg
// gprof cpi-pg

#include <stdio.h>
#include <math.h>
#include <unistd.h>    //optarg
#include <time.h>      //gettime, la possibilitÃ  di utilizzare la struct timespec Ã¨ grazie a questa libreria
#include <stdlib.h>
#include <omp.h>

void options(int argc, char * argv[]);
void usage(char * argv[]);
double f1 (long int);
double f2 (long int);

long int n=1000000000;    // numero di intervalli per l'INTEGRAZIONE
int s=0;                 // tempo sleep utilizzato per SIMULARE il codice NON PARALLELIZZABILE
double h; 		// Larghezza di ciascun INTERVALLO
char hostname[100]; 	// Stringa(o meglio char Array) che contiene il nome host della macchina

#define BILLION  1000000000L;

 double ta,tb,tc,td; // Sono variabili usate per calcolare quanto impiegano determinate parti di codice per essere ESEGUITE.
 double tnp; // Variabile utilizzata per calcolare il TEMPO DI ESECUZIONE COMPLESSIVO del PROGRAMMA, quindi sia le PARTI SEQUENZIALI che quelle PARALLELIZZABILI.
 int nt; // Rappresenta il numero di thread che verranno attivati nella REGIONE PARALLELA
 double sum1, sum2; // Contiene il risultato finale dei calcoli effettuati rispettivamente dalla FUNZIONE f1() e f2()
 double pi1, pi2; // Queste variabili vengono utilizzate per memorizzare i valori approssimati di Ï€ calcolati utilizzando i risultati parziali dei calcoli nelle funzioni f1() e f2() (che sono le variabili sum1 e sum2) rispettivamente.

/********************************************/

int main(int argc, char *argv[])
{
    nt = omp_get_max_threads();

    ta = omp_get_wtime(); // Questa funzione salva nella variabile "ta" il tempo corrente quando Ã¨ stata eseguita questa riga di codice.

    double  PI = 3.14159265358979323846264338327950288 ;

    gethostname(hostname, 100); 

    options(argc, argv);  /* optarg management */ 

    h = 1.0 / (double) n;

    sleep (s);  // Simulazione codice non paralellizzabile

    tb = omp_get_wtime(); // Questa funzione salva nella variabile "tb" il tempo corrente quando Ã¨ stata eseguita questa riga di codice.

    sum1= f1(n); // Contiene il risultato finale dei calcoli effettuati dalla FUNZIONE f1()

    tc = omp_get_wtime(); // Questa funzione salva nella variabile "tc" il tempo corrente quando Ã¨ stata eseguita questa riga di codice.

    sum2= f2(n); // Contiene il risultato finale dei calcoli effettuati dalla FUNZIONE f2()

    td = omp_get_wtime(); // Questa funzione salva nella variabile "td" il tempo corrente quando Ã¨ stata eseguita questa riga di codice.

    pi1 = 4 * h * sum1;
    pi2 = 4 * h * sum2;

    fprintf(stderr,"#Inter       numTheads        n       tnp       time1        time2       error1      error2       hostname \n");
    fprintf(stdout,"OMP, %ld, %d, %.4f,  %.4f,  %.4f, %.8e, %.8e, %s \n",
                nt, n, td - ta, tc - tb, td - tc, fabs(pi1-PI), fabs(pi2-PI), hostname);

    return 0;
}

// Questa funzione Ã¨ utilizzata per calcolare una stima dell'integrale utilizzando il metodo dei rettangoli, la funzione presa in esame in questo metodo Ã¨ diversa da quella del metodo f2() quindi i risultati saranno leggermente diversi.
double f1 (long int n )
 { 
    long int i; 
    double x, sum=0.0;

    #pragma omp parallel for private(x) reduction(+:sum) 
    for (i = 1; i <= n; i++)
    {
       x = h * ((double)i - 0.5);
       sum += sqrt(1-x*x) ;
    }
    return sum; 
 }


// Questa metodo, come f1() calcola il risultato dell'integrale di una funzione usando il metodo dei RETTANGOLI, l'integrale Ã¨ calcolato in un intervallo definito [0, 1]
 double f2 (long int n )
 {
    long int i; 
    double x, sum=0.0;

    #pragma omp parallel for private(x) reduction(+:sum)
    for (i = 1; i <= n; i++)
    {
       x = h * ((double)i - 0.5);
       sum += (1.0 / (1.0 + x*x));
    }
    return sum;
 }

/************************************************/

void options(int argc, char * argv[]) //Gestisce gli argomenti della riga di comando utilizzati per impostare il numero di intervalli (-n) e il tempo di sleep (-s).
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

void usage(char * argv[]) // Stampa un messaggio di utilizzo del programma, nel caso in cui non sia eseguito correttamente
{
  printf ("\n%s [-n intervals] [-s sleep] [-h]",argv[0]); 
  printf ("\n"); 
}
