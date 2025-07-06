#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_VALUES 5    // Número de valores por proceso
#define THRESHOLD 50    // Umbral crítico para la alerta

int main(int argc, char *argv[]) {
    int rank, size;
    int *data = NULL;
    double start_time, end_time;
    double local_sum = 0.0, local_avg;
    double *local_avgs = NULL;
    int i;

    // Inicialización de MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Cálculo del número total de elementos
    int total_elements = NUM_VALUES * size;

    // Comprobación de robustez: total_elements debe ser múltiplo de size
    if (total_elements % size != 0) {
        if (rank == 0) {
            fprintf(stderr, "Error: total_elements (%d) no es múltiplo de número de procesos (%d)\n", total_elements, size);
        }
        MPI_Finalize();
        return EXIT_FAILURE;
    }

    // El proceso 0 asigna y genera los datos
    if (rank == 0) {
        data = malloc(total_elements * sizeof(int));
        // Semilla basada en tiempo MPI para evitar <time.h>
        srand((unsigned)(MPI_Wtime() * 1000));
        for (i = 0; i < total_elements; i++) {
            data[i] = rand() % 100;  // Valores aleatorios entre 0 y 99
        }
    }

    // Cada proceso reserva espacio para sus datos locales
    int local_data[NUM_VALUES];

    // Sincronización antes de iniciar la medición de tiempo
    MPI_Barrier(MPI_COMM_WORLD);
    start_time = MPI_Wtime();

    // Distribución de datos a todos los procesos
    MPI_Scatter(data, NUM_VALUES, MPI_INT, local_data, NUM_VALUES, MPI_INT, 0, MPI_COMM_WORLD);

    // Cálculo de la suma y media local
    for (i = 0; i < NUM_VALUES; i++) {
        local_sum += local_data[i];
    }
    local_avg = local_sum / NUM_VALUES;

    // El proceso 0 reserva espacio para recopilar medias
    if (rank == 0) {
        local_avgs = malloc(size * sizeof(double));
    }

    // Recolección de las medias locales en el proceso 0
    MPI_Gather(&local_avg, 1, MPI_DOUBLE, local_avgs, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    end_time = MPI_Wtime();

    // Proceso 0 muestra resultados y alertas
    if (rank == 0) {
        printf("Tiempo de ejecución: %f segundos\n", end_time - start_time);
        printf("Medias locales calculadas:\n");
        for (i = 0; i < size; i++) {
            printf("Proceso %d: %.2f\n", i, local_avgs[i]);
        }
        printf("\nAlertas (media > %d):\n", THRESHOLD);
        for (i = 0; i < size; i++) {
            if (local_avgs[i] > THRESHOLD) {
                printf("Proceso %d con media %.2f\n", i, local_avgs[i]);
            }
        }
    }

    // Liberación de memoria y finalización de MPI
    if (data != NULL) free(data);
    if (local_avgs != NULL) free(local_avgs);

    MPI_Finalize();
    return 0;
}
