#include <stdio.h>
#include <omp.h>

int main() {
    long long N = 10000000000; // 10.000 millones
    double suma = 0.0;
    double start, end;

    start - omp_get_wtime();

    #pragma omp parallel for reduction(+:suma)
    for (long long i = 1; i <= N; i++) {
        suma += (i * 1.5) / (i + 1.0);
    }

    end = omp_get_wtime();

    printf("Resultado final: %.2f\n", suma);
    printf("Tiempo: %f segundos\n", end - start);
    return 0;
}
