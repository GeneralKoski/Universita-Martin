#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#define MIN_THREADS 5
#define MAX_THREADS 10

int n;
int t;
int* A;
int sum = 0;
pthread_mutex_t lock; //variabile di tipo mutex che protegge l'accesso a "sum"

void* sumArray(void* arg) {	//funzione che calcola la somma dei valori nell'array e usa "lock" per proteggere l'accesso a "sum"
    int thread_sum = 0;
    int thread_num = *((int*) arg);
    for (int i = 0; i < t; i++) {
        thread_sum += A[i];
    }
    pthread_mutex_lock(&lock);
    sum += thread_sum;
    pthread_mutex_unlock(&lock);
    return NULL;
}

int main() {
    struct timespec start, finish;
    double elapsed;
    clock_gettime(CLOCK_MONOTONIC, &start); //inizia a misurare il tempo

    printf("Inserire il numero di elementi dell'array: ");
    scanf("%d", &n);
    A = (int*) malloc(n * sizeof(int)); //il comando "malloc" alloca un nuovo spazio di memoria per memorizzare la variabile
    printf("Scrivi il numero di thread (da %d a %d): ", MIN_THREADS, MAX_THREADS);
    scanf("%d", &t);
    if (t < MIN_THREADS || t > MAX_THREADS) {
        printf("Numero non valido di thread.\n");
        return 1;
    }

    clock_gettime(CLOCK_MONOTONIC, &finish); //ferma la misurazione del tempo e calcolca il tempo trascorso dallo start con il comando "clock_gettime"
    elapsed = (finish.tv_sec - start.tv_sec);
    elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("Tempo trascorso per la creazione dell'array: %f\n", elapsed);

    clock_gettime(CLOCK_MONOTONIC, &start); //inizia a misurare di nuovo il tempo ma per la parte di codice successiva
    srand(time(NULL)); //comando per il random dei numeri
    for (int i = 0; i < n; i++) {
        A[i] = rand();
    }

    pthread_t threads[t]; //array di thread
    int thread_nums[t]; //array di numeri di thread
    pthread_mutex_init(&lock, NULL);
    for (int i = 0; i < t; i++) { //ciclo per creare i thread
        thread_nums[i] = i;
        pthread_create(&threads[i], NULL, sumArray, &thread_nums[i]);
    }
    for (int i = 0; i < t; i++) { //attende che tutti i thread terminino
        pthread_join(threads[i], NULL);
    }
    pthread_mutex_destroy(&lock); //distrugge la lock

    clock_gettime(CLOCK_MONOTONIC, &finish); //calcola il tempo trascorso dallo scorso start
    elapsed = (finish.tv_sec - start.tv_sec);
    elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0; //converto nanosecondi in secondi
    printf("Tempo impiegato: %f\n", elapsed);

    printf("La somma dei valori nell'array è: %d\n", sum);
    free(A); //libera la memoria allocata dinamicamente nell'array A
    return 0;
}

