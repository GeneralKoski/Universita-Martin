#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <math.h>
#include <mpi.h>

#define BILLION 1000000000L;

void options(int argc, char *argv[]);
void usage(char *argv[]);
double f1(long int, long int);
double f2(long int, long int);

long int n = 1000000000;  // intervalli
int s = 0;                // tempo sleep
double h;
char hostname[100];

double f1(long int, long int);
double f2(long int, long int);

/********************************************/

double sum1, sum2;
double pi1, pi2;

int main(int argc, char *argv[])
{
    double Lsum1, Lsum2;
    double start_time, end_time, tot_time_sum1, tot_time_sum2, avg_time_sum1, avg_time_sum2;
    
    // Gestione degli argomenti della linea di comando
    options(argc, argv);
    
    int mpiRank, mpiTasks;
    
    double PI = 3.14159265358979323846264338327950288;

    // Inizializzo MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &mpiRank); // mpiRank --> Contiene l'indice del task corrente
    MPI_Comm_size(MPI_COMM_WORLD, &mpiTasks); // mpiTasks --> Contiene il numero di task, che saranno specificati in fase di esecuzione

    long int sottodominio = n / mpiTasks;
    long int Lfirst = sottodominio * mpiRank + 1;
    long int Llast = sottodominio * mpiRank + sottodominio;
	  sum1 = 0.0;
	  sum2 = 0.0;

    // Ottengo il nome dell'host
    gethostname(hostname, 100);

    h = 1.0 / (double)n;

    sleep(s); // Simulazione codice non parallelizzabile


    start_time = MPI_Wtime();
    // Calcolo delle somme parziali
    Lsum1 = f1(Lfirst, Llast);
    // Riduzione delle somme parziali
    MPI_Reduce(&Lsum1, &sum1, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    end_time = MPI_Wtime();
    
    tot_time_sum1 = end_time - start_time;
    MPI_Reduce(&tot_time_sum1, &avg_time_sum1, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    
    start_time = MPI_Wtime();
    // Calcolo delle somme parziali
    Lsum2 = f2(Lfirst, Llast);
    // Riduzione delle somme parziali
    MPI_Reduce(&Lsum2, &sum2, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    end_time = MPI_Wtime();
    
    tot_time_sum2 = end_time - start_time;
    MPI_Reduce(&tot_time_sum2, &avg_time_sum2, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (mpiRank == 0)
    {
        avg_time_sum1 = avg_time_sum1 / mpiTasks;
        avg_time_sum2 = avg_time_sum2 / mpiTasks;
        
        pi1 = 4 * h * sum1;
        pi2 = 4 * h * sum2;

		fprintf(stderr,"#MPI, inter, tnp, avg_time_f1, avg_time_f2, error1, error2, hostname\n");
        fprintf(stdout, "MPI, %d, %ld,  %.5f,  %.5f,  %.5f, %.8e, %.8e, %s \n",
                mpiTasks, n, (s + avg_time_sum1 + avg_time_sum2), avg_time_sum1, avg_time_sum2, fabs(pi1 - PI), fabs(pi2 - PI), hostname);
    }

    MPI_Finalize();
    return 0;
}

double f1(long int Lfirst, long int Llast)
{
    long int i;
    double x, sum = 0.0;
    for (i = Lfirst; i <= Llast; i++)
    {
        x = h * ((double)i - 0.5);
        sum += sqrt(1 - x * x);
    }
    return sum;
}

double f2(long int Lfirst, long int Llast)
{
    long int i;
    double x, sum = 0.0;
    for (i = Lfirst; i <= Llast; i++)
    {
        x = h * ((double)i - 0.5);
        sum += (1.0 / (1.0 + x * x));
    }
    return sum;
}

void options(int argc, char *argv[])
{
    int i;
    while ((i = getopt(argc, argv, "n:s:h")) != -1)
    {
        switch (i)
        {
        case 'n':
            n = strtol(optarg, NULL, 10);
            break;
        case 's':
            s = strtol(optarg, NULL, 10);
            break;
        case 'h':
            usage(argv);
            exit(1);
        case '?':
            usage(argv);
            exit(1);
        default:
            usage(argv);
            exit(1);
        }
    }
}

void usage(char *argv[])
{
    printf("\n%s [-n intervals] [-s sleep] [-h]", argv[0]);
    printf("\n");
}
