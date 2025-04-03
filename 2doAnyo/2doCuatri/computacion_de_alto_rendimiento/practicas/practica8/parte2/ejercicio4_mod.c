#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank, maxRank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Reduce(&rank, &maxRank, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        printf("Proceso %d, máximo de ranks: %d\n", rank, maxRank);
    }

    MPI_Finalize();
    return 0;
}
