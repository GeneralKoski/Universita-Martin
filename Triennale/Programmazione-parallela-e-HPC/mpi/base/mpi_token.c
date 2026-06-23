#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv)
{
    MPI_Status status;
    int rank, size;
    int prev_rank, next_rank;

    int token;  /* token to communicate */

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    prev_rank = (rank-1+size) % size;
    next_rank = (rank+1)      % size;

    // Inizializza il token
    token = 0;
    if (rank == 0) {
        token = 1;  // Task 0 inizia con il token
    }

    // Inizia la circolazione del token
    do {
        // Il task 0 invia il token al next_rank e riceve il token da prev_rank
        if (rank == 0) {
            MPI_Sendrecv(&token, 1, MPI_INT, next_rank, 666,
                         &token, 1, MPI_INT, prev_rank, 666, MPI_COMM_WORLD, &status);
        } else {
            // Gli altri task ricevono il token da prev_rank e lo inviano a next_rank
            MPI_Recv(&token, 1, MPI_INT, prev_rank, 666, MPI_COMM_WORLD, &status);
            printf("Process %d receives token %d from process %d.\n", rank, token, status.MPI_SOURCE);
            MPI_Send(&token, 1, MPI_INT, next_rank, 666, MPI_COMM_WORLD);
        }
    } while (rank != 0 || token == 1); // Continua finché il token non torna al task 0

    if (rank == 0) {
        // Il task 0 riceve il token indietro e termina
        MPI_Recv(&token, 1, MPI_INT, prev_rank, 666, MPI_COMM_WORLD, &status);
        printf("Process %d receives token %d from process %d and terminates.\n", rank, token, status.MPI_SOURCE);
    }

    MPI_Finalize();
    return 0;
}
