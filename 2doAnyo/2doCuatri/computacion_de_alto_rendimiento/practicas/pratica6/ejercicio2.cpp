#include <stdio.h>
#include <omp.h>

int main() {
    long long N = 1000000000; // 1.000 millones
    double suma = 0.0;
    double start, end;

    start = omp_get_wtime();

    #pragma omp parallel for
    for (long long i = 1; i <= N; i++) {
        double valor = (i * 1.5) / (i + 1.0);
        #pragma omp critical
        {
            suma += valor;
        }
    }

    end = omp_get_wtime();

    printf("Resultado final: %.2f\n", suma);
    printf("Tiempo: %f segundos\n", end - start);
    return 0;
}
