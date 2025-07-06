
#include <mpi.h>
#include <stdio.h> 
int main(int argc, char** argv) { 
 MPI_Init(&argc, &argv); 
 int rank, size; 
 MPI_Comm_rank(MPI_COMM_WORLD, &rank); 
 MPI_Comm_size(MPI_COMM_WORLD, &size); 
 if (rank == 0) { 
 int dato = 0; 
 MPI_Send(&dato, 1, MPI_INT, 1, 0, MPI_COMM_WORLD); 
 } else { 
 int recibido; 
 MPI_Recv(&recibido, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, 
MPI_STATUS_IGNORE); 
 recibido++; 
 if (rank < size - 1) { 
 MPI_Send(&recibido, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD); 
 } else { 
 printf("Valor final: %d\n", recibido); 
 } 
 } 
 MPI_Finalize(); 
 return 0; 
}