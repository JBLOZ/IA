#include <mpi.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    int rank, size;

    // Inicializa MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // Obtiene el identificador del proceso
    MPI_Comm_size(MPI_COMM_WORLD, &size);  // Obtiene el número total de procesos

    // Cada proceso imprime un mensaje
    printf("Hola mundo desde el proceso %d de %d\n", rank, size);

    // Finaliza MPI
    MPI_Finalize();
    return 0;
}
