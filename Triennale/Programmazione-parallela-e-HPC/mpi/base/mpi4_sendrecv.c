#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv)
{
 MPI_Status status;
 int rank, size;
 int prev_rank, next_rank;

 int data_send, data_recv;  /* data to communicate */

 MPI_Init(&argc, &argv);
 MPI_Comm_rank(MPI_COMM_WORLD, &rank);
 MPI_Comm_size(MPI_COMM_WORLD, &size);

 prev_rank = (rank-1+size) % size;
 next_rank = (rank+1)      % size;

 data_send = rank;

 MPI_Sendrecv(&data_send, 1, MPI_INT, next_rank, 666, 
              &data_recv, 1, MPI_INT, prev_rank, 666, MPI_COMM_WORLD, &status);

  printf("Process %d/%d receives %d from process %d.\n", rank, size, data_recv, status.MPI_SOURCE);

 MPI_Finalize();
 return 0;
}
