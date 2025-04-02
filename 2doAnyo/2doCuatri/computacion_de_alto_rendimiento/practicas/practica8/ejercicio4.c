#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank, suma;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Reduce(&rank, &suma, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD); // Suma de ranks
    if (rank == 0) printf("Suma de ranks: %d\n", suma);
    MPI_Finalize();
    return 0;
}
