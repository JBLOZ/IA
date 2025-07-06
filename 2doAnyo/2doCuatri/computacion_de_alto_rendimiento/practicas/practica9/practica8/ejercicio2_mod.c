#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0) {
        int dato = 10;  // Dato inicial modificado a 10
        // Imprimir el dato inicial en el proceso 0
        printf("Proceso 0 inicia con: %d\n", dato);
        MPI_Send(&dato, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
    } else {
        int recibido;
        // Cada proceso recibe el dato del proceso anterior
        MPI_Recv(&recibido, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        // Incrementa el dato en 2
        recibido += 2;
        // Si no es el último proceso, se envía al siguiente; de lo contrario, se imprime el resultado final
        if (rank < size - 1) {
            MPI_Send(&recibido, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD);
        } else {
            printf("Valor final en el proceso %d: %d\n", rank, recibido);
        }
    }

    MPI_Finalize();
    return 0;
}
