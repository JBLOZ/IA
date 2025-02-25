#include <iostream>
#include <omp.h>

int main() {
    // ==============================
    // Ejercicio 1: Condición de carrera y atomic
    // ==============================
    long long var_no_atomic = 0;
    long long var_atomic = 0;
    const long long iterations_ex1 = 100000000;  // 100 millones de iteraciones

    double t1_start, t1_end, tiempo_no_atomic;
    double t2_start, t2_end, tiempo_atomic;

    // Incremento sin protección: se produce condición de carrera
    t1_start = omp_get_wtime();
    #pragma omp parallel for
    for (long long i = 0; i < iterations_ex1; i++) {
        var_no_atomic++;
    }
    t1_end = omp_get_wtime();
    tiempo_no_atomic = t1_end - t1_start;

    // Incremento con protección usando #pragma omp atomic
    t2_start = omp_get_wtime();
    #pragma omp parallel for
    for (long long i = 0; i < iterations_ex1; i++) {
        #pragma omp atomic
        var_atomic++;
    }
    t2_end = omp_get_wtime();
    tiempo_atomic = t2_end - t2_start;

    std::cout << "----- Ejercicio 1: Condición de carrera y atomic -----" << std::endl;
    std::cout << "Sin protección (condición de carrera):" << std::endl;
    std::cout << "  Valor final: " << var_no_atomic << std::endl;
    std::cout << "  Tiempo de ejecución: " << tiempo_no_atomic << " segundos" << std::endl;
    std::cout << std::endl;
    std::cout << "Con #pragma omp atomic:" << std::endl;
    std::cout << "  Valor final: " << var_atomic << std::endl;
    std::cout << "  Tiempo de ejecución: " << tiempo_atomic << " segundos" << std::endl;

    // ==============================
    // Ejercicio 2: Acumulación segura con reduction
    // ==============================
    const long long N = 1000000; // Sumar números del 1 al 1,000,000
    long long suma_seq = 0;
    long long suma_parallel_naive = 0;
    long long suma_parallel_reduction = 0;

    double seq_start, seq_end, tiempo_seq;
    double paralela_naive_start, paralela_naive_end, tiempo_naive;
    double reduction_start, reduction_end, tiempo_reduction;

    // 1. Acumulación secuencial
    seq_start = omp_get_wtime();
    for (long long i = 1; i <= N; i++) {
        suma_seq += i;
    }
    seq_end = omp_get_wtime();
    tiempo_seq = seq_end - seq_start;

    // 2. Acumulación paralela sin protección (sin reduction) – problema de condición de carrera
    paralela_naive_start = omp_get_wtime();
    #pragma omp parallel for
    for (long long i = 1; i <= N; i++) {
        suma_parallel_naive += i;  // Esta suma no está sincronizada
    }
    paralela_naive_end = omp_get_wtime();
    tiempo_naive = paralela_naive_end - paralela_naive_start;

    // 3. Acumulación paralela con reduction (solución segura)
    reduction_start = omp_get_wtime();
    #pragma omp parallel for reduction(+:suma_parallel_reduction)
    for (long long i = 1; i <= N; i++) {
        suma_parallel_reduction += i;
    }
    reduction_end = omp_get_wtime();
    tiempo_reduction = reduction_end - reduction_start;

    // Valor esperado (fórmula de la suma de una progresión aritmética)
    long long esperado = (N * (N + 1)) / 2;
    double speedup = tiempo_seq / tiempo_reduction; // Speed-up de reduction vs secuencial

    std::cout << "\n----- Ejercicio 2: Acumulación segura con reduction -----" << std::endl;
    std::cout << "Acumulación secuencial:" << std::endl;
    std::cout << "  Suma: " << suma_seq << std::endl;
    std::cout << "  Tiempo de ejecución: " << tiempo_seq << " segundos" << std::endl;
    std::cout << std::endl;
    std::cout << "Acumulación paralela sin reduction (no segura):" << std::endl;
    std::cout << "  Suma: " << suma_parallel_naive << " (resultado incorrecto, puede variar)" << std::endl;
    std::cout << "  Tiempo de ejecución: " << tiempo_naive << " segundos" << std::endl;
    std::cout << std::endl;
    std::cout << "Acumulación paralela con reduction:" << std::endl;
    std::cout << "  Suma: " << suma_parallel_reduction << std::endl;
    std::cout << "  Tiempo de ejecución: " << tiempo_reduction << " segundos" << std::endl;
    std::cout << std::endl;
    std::cout << "Valor esperado: " << esperado << std::endl;
    std::cout << "Speed-up (secuencial / reduction): " << speedup << std::endl;

    return 0;
}
