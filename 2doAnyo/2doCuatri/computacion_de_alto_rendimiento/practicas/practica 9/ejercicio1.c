#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUM_VALUES 5    // Número de valores por proceso
#define THRESHOLD 50    // Umbral crítico para la alerta

int main(int argc, char *argv[]) {
    int rank, size;
    int *data = NULL;
    double local_sum = 0, local_avg;
    double *local_avgs = NULL;
    int i;
    
    // Inicialización de MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    // Número total de elementos (debe ser múltiplo del número de procesos)
    int total_elements = NUM_VALUES * size;
    
    // Solo el proceso 0 genera el array de datos
    if (rank == 0) {
        data = malloc(total_elements * sizeof(int));
        srand(time(NULL));
        for (i = 0; i < total_elements; i++) {
            data[i] = rand() % 100; // Valores aleatorios entre 0 y 99
        }
    }
    
    // Cada proceso recibirá NUM_VALUES enteros
    int local_data[NUM_VALUES];
    
    // Distribución de datos: MPI_Scatter reparte el array a todos los procesos
    MPI_Scatter(data, NUM_VALUES, MPI_INT, local_data, NUM_VALUES, MPI_INT, 0, MPI_COMM_WORLD);
    
    // Cada proceso calcula la suma y la media de sus valores locales
    for (i = 0; i < NUM_VALUES; i++) {
        local_sum += local_data[i];
    }
    local_avg = local_sum / NUM_VALUES;
    
    // Sincronización antes de proceder a recopilar resultados (opcional)
    MPI_Barrier(MPI_COMM_WORLD);
    
    // El proceso 0 reservará espacio para recibir las medias locales
    if (rank == 0) {
        local_avgs = malloc(size * sizeof(double));
    }
    
    // Recolección de las medias locales en el proceso 0
    MPI_Gather(&local_avg, 1, MPI_DOUBLE, local_avgs, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    // El proceso 0 muestra los resultados y detecta alertas
    if (rank == 0) {
        printf("Medias locales calculadas:\n");
        for (i = 0; i < size; i++) {
            printf("Proceso %d: %.2f\n", i, local_avgs[i]);
        }
        printf("\nAlertas: Procesos con promedio mayor a %d:\n", THRESHOLD);
        for (i = 0; i < size; i++) {
            if (local_avgs[i] > THRESHOLD) {
                printf("Proceso %d con promedio %.2f\n", i, local_avgs[i]);
            }
        }
    }
    
    // Liberación de memoria y finalización de MPI
    if (data != NULL) free(data);
    if (local_avgs != NULL) free(local_avgs);
    
    MPI_Finalize();
    return 0;
}
