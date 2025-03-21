#include <stdio.h>
#include <omp.h>
#include <vector>

int main() {
    // Número de iteraciones (aproximadamente 10.000 millones)
    long long N = 10000060000LL;

    // Vector con el número de hilos a utilizar
    std::vector<int> hilos {1, 2, 4, 8, 16};

    // Fracción paralelizable para la Ley de Amdahl (95% paralelizable, por ejemplo)
    double f = 0.95;

    // Tamaño del chunk para el scheduling
    int chunk = 1;

    // Array de schedules a evaluar
    const int numSchedules = 3;
    const char* scheduleNames[numSchedules] = {"static", "dynamic", "guided"};

    // Se generan tres tablas, una para cada tipo de schedule
    for (int sch = 0; sch < numSchedules; sch++) {
        // Imprime la cabecera de la tabla para el schedule actual
        printf("\n****************************\n");
        printf("Schedule: %s\n", scheduleNames[sch]);
        printf("****************************\n");
        printf("%-10s %-15s %-12s %-12s %-15s\n", "Hilos", "Tiempo(s)", "SpeedUp", "Eficiencia", "SpeedUp Amdahl");

        double baseline_time = 0.0; // Tiempo base para 1 hilo (se actualizará en cada tabla)

        // Bucle para recorrer la cantidad de hilos
        for (auto num_threads : hilos) {
            double suma = 0.0;
            double start, end, t;

            // Configuramos el número de hilos para la región paralela
            omp_set_num_threads(num_threads);

            start = omp_get_wtime();
            // Según el schedule (static, dynamic o guided) usamos la directiva correspondiente
            if (sch == 0) {
                #pragma omp parallel for schedule(static, chunk) reduction(+:suma)
                for (long long i = 1; i <= N; i++) {
                    suma += (1 * 1.5) / (i + 1.0);
                }
            } else if (sch == 1) {
                #pragma omp parallel for schedule(dynamic, chunk) reduction(+:suma)
                for (long long i = 1; i <= N; i++) {
                    suma += (1 * 1.5) / (i + 1.0);
                }
            } else if (sch == 2) {
                #pragma omp parallel for schedule(guided, chunk) reduction(+:suma)
                for (long long i = 1; i <= N; i++) {
                    suma += (1 * 1.5) / (i + 1.0);
                }
            }
            end = omp_get_wtime();
            t = end - start;

            // Para el cálculo del speedup experimental usamos el tiempo para 1 hilo como baseline
            if (num_threads == 1)
                baseline_time = t;

            double speedup = baseline_time / t;
            double eficiencia = speedup / num_threads;
            double speedup_amdahl = 1.0 / ((1 - f) + (f / num_threads));

            // Imprime la fila de la tabla
            printf("%-10d %-15f %-12f %-12f %-15f\n", num_threads, t, speedup, eficiencia, speedup_amdahl);
        } // Fin del bucle de hilos

        printf("\n");
    } // Fin del bucle de schedules

    return 0;
}
