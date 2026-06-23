#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/wait.h>

int main() {
    int n, p, i, j;
    printf("Inserire il numero di elementi dell'array: ");
    scanf("%d", &n);
    printf("Inserire il numero di processi (da 5 a 10): ");
    scanf("%d", &p);

    if (p < 5 || p > 10) {
        printf("Numero non valido di processi.\n");
        return 1;
    }

    int A[n];
    int somma_parziale[p];

    srand(time(NULL));
    for (i = 0; i < n; i++) { //creazione dell'array con valori casuali
        A[i] = rand();
    }

    int fd[p][2];
    pid_t pid;
    clock_t t_inizio, t_fine;

    t_inizio = clock();
    for (i = 0; i < p; i++) { //creazione dei processi
        pipe(fd[i]);
        pid = fork();
        if (pid == 0) {
            somma_parziale[i] = 0;
            for (j = (n/p)*i; j < (n/p)*(i+1); j++) { //calcolo della somma parziale
                somma_parziale[i] += A[j];
            }
            //invio della somma parziale al processo padre
            close(fd[i][0]);
            write(fd[i][1], &somma_parziale[i], sizeof(int));
            close(fd[i][1]);
            exit(0);
        }
    }

    int somma_totale = 0;
    for (i = 0; i < p; i++) { //calcolo della somma totale e attesa dei processi figli
        wait(NULL);
        close(fd[i][1]);
        read(fd[i][0], &somma_parziale[i], sizeof(int));
        somma_totale += somma_parziale[i];
        close(fd[i][0]);
    }
    t_fine = clock();
    printf("La somma dei valori nell'array è: %d\n", somma_totale);
    printf("Tempo impiegato: %f\n", (double)(t_fine - t_inizio) / CLOCKS_PER_SEC);

    return 0;
}

