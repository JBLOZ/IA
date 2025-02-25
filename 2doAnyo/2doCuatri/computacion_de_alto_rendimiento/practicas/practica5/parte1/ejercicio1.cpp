#include <iostream>
#include <chrono>
#include <omp.h>

using namespace std;
using namespace std::chrono;

int main() {
    // Número de iteraciones para cada bucle
    const long iterations = 100000000;

    // Variable global para la versión sin protección
    long global_unprotected = 0;
    // Variable global para la versión con protección atomic
    long global_atomic = 0;

    // Medición del tiempo para la versión sin protección
    auto start_unprotected = high_resolution_clock::now();
    #pragma omp parallel for
    for (long i = 0; i < iterations; i++) {
        // Incremento sin protección: puede producir una condición de carrera
        global_unprotected++;
    }
    auto end_unprotected = high_resolution_clock::now();
    auto duration_unprotected = duration_cast<milliseconds>(end_unprotected - start_unprotected).count();

    // Medición del tiempo para la versión con #pragma omp atomic
    auto start_atomic = high_resolution_clock::now();
    #pragma omp parallel for
    for (long i = 0; i < iterations; i++) {
        // Incremento protegido con directiva atomic para evitar la condición de carrera
        #pragma omp atomic
        global_atomic++;
    }
    auto end_atomic = high_resolution_clock::now();
    auto duration_atomic = duration_cast<milliseconds>(end_atomic - start_atomic).count();

    // Impresión de resultados
    cout << endl << "==== Sin protección (condición de carrera) ====" << endl;
    cout << "Valor final (esperado " << iterations << "): " << global_unprotected << endl;
    cout << "Tiempo de ejecución: " << duration_unprotected << " ms" << endl << endl;

    cout << "==== Con #pragma omp atomic ====" << endl;
    cout << "Valor final: " << global_atomic << endl;
    cout << "Tiempo de ejecución: " << duration_atomic << " ms" << endl;

    return 0;
}
