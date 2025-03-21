#include <stdio.h>
#include <omp.h>

int main() {
    double resultado_final = 0.0;
    double start, end;

    start = omp_get_wtime();

    #pragma omp parallel for reduction(+:resultado_final) schedule(dynamic, 1)
    for (int i = 0; i < 16; i++) {
        double local_result = 0.0;
        long long carga = 100000000 * (i % 4 + 1); // Cargas desiguales
        for (long long j = 0; j < carga; j++) {
            local_result += (j * 0.5) / (j + 1.0); // Cálculo sencillo que evita optimización excesiva
        }
        resultado_final += local_result;
    }
    end = omp_get_wtime();

    printf("Resultado final: %.2f\n", resultado_final);
    printf("Tiempo: %f segundos\n", end - start);

    return 0;
