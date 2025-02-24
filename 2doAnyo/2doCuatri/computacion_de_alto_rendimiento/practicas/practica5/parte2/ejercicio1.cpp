#include <ctime>
#include <iostream>
#include <omp.h>
#define N 1000000
using namespace std;

int main() {
    long long suma = 0;
    double start, end;
    double time_seq, time_par_no_red, time_par_red;

    // ---------------------------
    // Versión Secuencial
    // ---------------------------
    start = omp_get_wtime();
    for (int i = 1; i <= N; i++) {
        suma += i;
    }
    end = omp_get_wtime();
    time_seq = end - start;
    cout << endl << "Secuencial - Suma: " << suma << " Tiempo: " << time_seq << " segundos" << endl;

    // ---------------------------
    // Versión Paralela sin reduction
    // (Se observa condición de carrera: resultado erróneo)
    // ---------------------------
    suma = 0;
    start = omp_get_wtime();
    #pragma omp parallel for
    for (int i = 1; i <= N; i++) {
        suma += i;  // Varias hebras modifican 'suma' sin sincronización
    }
    end = omp_get_wtime();
    time_par_no_red = end - start;
    cout << "Paralela sin reduction - Suma: " << suma << " Tiempo: " << time_par_no_red << " segundos" << endl;

    // ---------------------------
    // Versión Paralela con reduction
    // (Se corrige la condición de carrera)
    // ---------------------------
    suma = 0;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:suma)
    for (int i = 1; i <= N; i++) {
        suma += i;
    }
    end = omp_get_wtime();
    time_par_red = end - start;
    cout << "Paralela con reduction - Suma: " << suma << " Tiempo: " << time_par_red << " segundos" << endl;

    // ---------------------------
    // Análisis
    // ---------------------------
    // Problema en la versión paralela sin reduction:
    //   - La variable 'suma' es compartida por todos los hilos sin sincronización, lo que
    //     provoca condiciones de carrera y un resultado final erróneo.
    //
    // Con reduction:
    //   - Cada hilo mantiene una copia local de la variable 'suma' y al finalizar se combinan,
    //     garantizando un resultado correcto sin la sobreescritura simultánea.
    //
    // Cálculo del Speed-up (tiempo secuencial / tiempo con reduction):
    double speedup_red = time_seq / time_par_red;
    double speedup_non_red = time_seq / time_par_no_red;
    cout << endl << "Speed-up (secuencial / reduction): " << speedup_red << endl;
    cout << "Speed-up (secuelcial / non_reduction): " << speedup_non_red << endl << endl;

    return 0;
}
