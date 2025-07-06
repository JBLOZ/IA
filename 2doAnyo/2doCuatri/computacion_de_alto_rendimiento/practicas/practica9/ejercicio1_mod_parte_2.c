#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    if (rank == 0) {
        int dato = 42; // Valor a enviar
        MPI_Send(&dato, 1, MPI_INT, 2, 0, MPI_COMM_WORLD);
    } else if (rank == 2) {
        int recibido;
        // Recibimos el dato enviado por el proceso 0
        MPI_Recv(&recibido, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        // Multiplicamos el dato por 3
        int resultado = recibido * 3;
        printf("Proceso 2 recibió %d y al multiplicarlo por 3 da: %d\n", recibido, resultado);
    }
    MPI_Finalize();
    return 0;
}