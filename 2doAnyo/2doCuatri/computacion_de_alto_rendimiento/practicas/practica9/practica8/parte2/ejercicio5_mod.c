#include <mpi.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    if (rank % 2 == 0) { // Esperamos 2 segundos en los rangos pares
        sleep(2);
    }
    double t1 = MPI_Wtime();
    MPI_Barrier(MPI_COMM_WORLD); // Sincronización
    double t2 = MPI_Wtime();
    printf("Proceso %d: Tiempo = %f\n", rank, t2 - t1);
    MPI_Finalize();
    return 0;
}
