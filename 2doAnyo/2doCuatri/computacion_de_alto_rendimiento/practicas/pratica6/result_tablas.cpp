#include <iostream>
#include <cstdio>
#include <vector>
#include <omp.h>

using namespace std;

struct ResultE1 {
    int    numThreads;
    double timeSec;
    double speedup;
    double efficiency;
};

vector<ResultE1> runEjercicio1()
{
    cout << "======================== Ejercicio 1 ========================\n";


    long long N = 10000000000;

    // Valores de hilos a probar
    vector<int> threadsTest = {1, 2, 4, 8, 16};
    vector<double> tiempos(threadsTest.size());

    // Primero medimos con 1 hilo para luego calcular speedup
    for (size_t i = 0; i < threadsTest.size(); i++)
    {
        int nth = threadsTest[i];
        omp_set_num_threads(nth);

        double start = omp_get_wtime();
        double suma  = 0.0;

        #pragma omp parallel for reduction(+:suma)
        for (long long j = 1; j <= N; j++) {
            suma += (j * 1.5) / (j + 1.0);
        }
        double end = omp_get_wtime();
        tiempos[i] = end - start;
    }

    // Generamos la tabla de resultados en memoria
    vector<ResultE1> resultados;
    double T1 = tiempos[0]; // tiempo con 1 hilo
    for (size_t i = 0; i < threadsTest.size(); i++)
    {
        ResultE1 r;
        r.numThreads = threadsTest[i];
        r.timeSec    = tiempos[i];
        r.speedup    = T1 / tiempos[i];
        r.efficiency = r.speedup / threadsTest[i];
        resultados.push_back(r);
    }

    // Impresión de la tabla solicitada
    cout << "Tabla de resultados (Ejercicio 1):\n";
    printf("%-10s %-12s %-12s %-12s\n", "Hilos(N)", "T_N (s)", "Speed-up", "Efic.E");
    for (auto &r: resultados) {
        printf("%-10d %-12.4f %-12.2f %-12.2f\n",
               r.numThreads, r.timeSec, r.speedup, r.efficiency);
    }
    cout << endl;

    return resultados; // Devolvemos para poder comparar en Ejercicio 4
}

// -----------------------------------------------------------------------------
// Ejercicio 2
// -----------------------------------------------------------------------------
//
// Compara tiempos usando 3 técnicas de sincronización:
//   1) critical
//   2) atomic
//   3) reduction
//
// Se miden con 1,2,4,8,16 hilos.
//
void runEjercicio2()
{
    cout << "======================== Ejercicio 2 ========================\n";

    // Reducimos N para la DEMO
    long long N = 1000000000;

    vector<int> threadsTest = {1, 2, 4, 8, 16};
    // Almacenarán los tiempos (critical, atomic, reduction) para cada #hilos
    vector<double> tCritical(threadsTest.size());
    vector<double> tAtomic  (threadsTest.size());
    vector<double> tReduction(threadsTest.size());

    // --- 1) critical ---
    for (size_t i = 0; i < threadsTest.size(); i++)
    {
        omp_set_num_threads(threadsTest[i]);

        double start = omp_get_wtime();
        double suma  = 0.0;
        #pragma omp parallel for
        for (long long j = 1; j <= N; j++)
        {
            double valor = (j * 1.5) / (j + 1.0);
            #pragma omp critical
            {
                suma += valor;
            }
        }
        double end = omp_get_wtime();
        tCritical[i] = end - start;
    }

    // --- 2) atomic ---
    for (size_t i = 0; i < threadsTest.size(); i++)
    {
        omp_set_num_threads(threadsTest[i]);

        double start = omp_get_wtime();
        double suma = 0.0;
        #pragma omp parallel for
        for (long long j = 1; j <= N; j++)
        {
            double valor = (j * 1.5) / (j + 1.0);
            #pragma omp atomic
            suma += valor;
        }
        double end = omp_get_wtime();
        tAtomic[i] = end - start;
    }

    // --- 3) reduction ---
    for (size_t i = 0; i < threadsTest.size(); i++)
    {
        omp_set_num_threads(threadsTest[i]);

        double start = omp_get_wtime();
        double suma  = 0.0;
        #pragma omp parallel for reduction(+:suma)
        for (long long j = 1; j <= N; j++)
        {
            double valor = (j * 1.5) / (j + 1.0);
            suma += valor;
        }
        double end = omp_get_wtime();
        tReduction[i] = end - start;
    }

    // Impresión comparativa
    cout << "Tabla de resultados (Ejercicio 2):\n";
    printf("%-10s %-12s %-12s %-12s\n", "Hilos", "Critical(s)", "Atomic(s)", "Reduction(s)");
    for (size_t i = 0; i < threadsTest.size(); i++)
    {
        printf("%-10d %-12.4f %-12.4f %-12.4f\n",
               threadsTest[i], tCritical[i], tAtomic[i], tReduction[i]);
    }
    cout << endl;

    // Aquí podrías calcular Speed-up análogo al Ejercicio 1, si lo deseas.
    // Por brevedad, solo se muestran los tiempos comparados.
}

// -----------------------------------------------------------------------------
// Ejercicio 3
// -----------------------------------------------------------------------------
//
// Se analiza el uso de distintos schedules: static, dynamic(1), guided.
// Se miden los tiempos con 4 y 8 hilos (p.ej.) para ver cuál schedule
// soporta mejor el desbalance de carga.
//
void runEjercicio3()
{
    cout << "======================== Ejercicio 3 ========================\n";

    // Para simular el comportamiento del original:
    //   - Calcularemos 16 "bloques", cada uno con una carga diferente
    //     (similar a la idea en el ejercicio).
    //   - Mantenemos la misma ecuación del ejemplo: local_result += (j * 0.5)/(j + 1.0)

    // schedules a comparar
    vector<string> schedules = {"static", "dynamic", "guided"};
    // Cantidad de hilos a probar (ahora sí incluye 16)
    vector<int> threadsTest = {4, 8, 16};

    // Resultados: un map [schedule][nThreads] = tiempo
    // Lo representamos con un simple diccionario encadenado,
    // aunque en C++ se podría usar std::map o algo similar.
    // Aquí haremos un vector 2D: [i_sch][i_thr].
    vector<vector<double>> resultados(schedules.size(), vector<double>(threadsTest.size()));

    // Recorremos schedules
    for (size_t sc = 0; sc < schedules.size(); sc++)
    {
        for (size_t th = 0; th < threadsTest.size(); th++)
        {
            omp_set_num_threads(threadsTest[th]);

            double start = omp_get_wtime();
            double resultado_final = 0.0;

            #pragma omp parallel
            {
                #pragma omp for reduction(+:resultado_final) \
                                schedule(static) nowait
                for (int i = 0; i < 0; i++) {
                    // NO-OP: este bloque no se va a ejecutar,
                    // solo para demostrar la sintaxis condicional.
                }
            }

            // Para poder cambiar el schedule en tiempo de ejecución,
            // debemos poner la directiva dentro de una macro o if.
            // Para simplificar, repetimos manualmente según el schedule.
            if (schedules[sc] == "static")
            {
                #pragma omp parallel for reduction(+:resultado_final) schedule(static)
                for (int i = 0; i < 16; i++) {
                    long long carga = 1000000000 * (i % 4 + 1);
                    double local_result = 0.0;
                    for (long long j = 0; j < carga; j++) {
                        local_result += (j * 0.5) / (j + 1.0);
                    }
                    resultado_final += local_result;
                }
            }
            else if (schedules[sc] == "dynamic")
            {
                #pragma omp parallel for reduction(+:resultado_final) schedule(dynamic, 1)
                for (int i = 0; i < 16; i++) {
                    long long carga = 1000000000 * (i % 4 + 1);
                    double local_result = 0.0;
                    for (long long j = 0; j < carga; j++) {
                        local_result += (j * 0.5) / (j + 1.0);
                    }
                    resultado_final += local_result;
                }
            }
            else // guided
            {
                #pragma omp parallel for reduction(+:resultado_final) schedule(guided)
                for (int i = 0; i < 16; i++) {
                    long long carga = 1000000000 * (i % 4 + 1);
                    double local_result = 0.0;
                    for (long long j = 0; j < carga; j++) {
                        local_result += (j * 0.5) / (j + 1.0);
                    }
                    resultado_final += local_result;
                }
            }

            double end = omp_get_wtime();
            resultados[sc][th] = end - start;
        }
    }

    // Imprimimos resultados en tabla
    cout << "Tabla de resultados (Ejercicio 3):\n";

    // Agregamos la columna de 16 hilos en el encabezado
    printf("%-10s  %-10s  %-10s  %-10s\n", "Schedule", "4 hilos (s)", "8 hilos (s)", "16 hilos (s)");

    // Ahora imprimimos los 3 valores para cada schedule
    for (size_t sc = 0; sc < schedules.size(); sc++) {
        printf("%-10s  %-12.4f %-12.4f %-12.4f\n",
               schedules[sc].c_str(),
               resultados[sc][0],
               resultados[sc][1],
               resultados[sc][2]);
    }
    cout << endl;
}

// -----------------------------------------------------------------------------
// Ejercicio 4
// -----------------------------------------------------------------------------
//
// Ley de Amdahl: donde p = 0.85 (85% paralelizable).
//   Speed-up teórico infinito: S_infty = 1 / (1 - p)
//   Speed-up teórico con N hilos: S(N) = 1 / ((1 - p) + p/N)
//
// Se comparan con Speed-ups reales del Ejercicio 1 (si se guardaron).
//
void runEjercicio4(const vector<ResultE1> &resE1)
{
    cout << "======================== Ejercicio 4 ========================\n";

    double p = 0.85; // fracción paralelizable
    // Speedup max teórico (hilos infinitos)
    double S_infty = 1.0 / (1.0 - p);

    // Vamos a calcular Speed-up teórico para hilos = 4 y 8
    auto speedupTheoretical = [&](int N) {
        return 1.0 / ((1.0 - p) + p / N);
    };
    double s4 = speedupTheoretical(4);
    double s8 = speedupTheoretical(8);

    cout << " - p = 0.85\n";
    cout << " - Speed-up teórico con hilos infinitos = " << S_infty << "\n";
    cout << " - Speed-up teórico (4 hilos) = " << s4 << "\n";
    cout << " - Speed-up teórico (8 hilos) = " << s8 << "\n\n";

    // Extraemos Speed-up real de Ejercicio 1 para 4 y 8 hilos
    // en la tabla de resE1
    double speedupReal4 = 0.0;
    double speedupReal8 = 0.0;
    for (auto &r : resE1) {
        if (r.numThreads == 4) {
            speedupReal4 = r.speedup;
        }
        if (r.numThreads == 8) {
            speedupReal8 = r.speedup;
        }
    }

    cout << "Velocidades Reales (tomadas de Ejercicio 1):\n";
    cout << " - Speed-up real (4 hilos) = " << speedupReal4 << "\n";
    cout << " - Speed-up real (8 hilos) = " << speedupReal8 << "\n\n";

    cout << "Conclusión: Compara si el Speed-up real se acerca al teórico.\n";
    cout << "            En la práctica, siempre hay overhead y no se\n";
    cout << "            suele llegar exactamente al límite teórico.\n";
    cout << endl;
}

// -----------------------------------------------------------------------------
// Ejercicio 5 (Opcional): Escalabilidad Débil
// -----------------------------------------------------------------------------
//
// Para cada número de hilos 1,2,4,8, se procesa 10,000 millones * (# hilos).
// Se mide si el tiempo permanece aproximadamente constante.
//
// Nota: aquí se reduce la carga para la DEMO.
//       En tu práctica real, usa 10,000 millones * (# hilos) si deseas.
//
void runEjercicio5()
{
    cout << "======================== Ejercicio 5 ========================\n";
    cout << "Escalabilidad débil: para N hilos -> 10,000 millones * N elementos.\n"
         << "(En esta demo se reduce el valor de 10,000 millones.)\n\n";

    vector<int> threadsTest = {1, 2, 4, 8};
    vector<double> tiempos(threadsTest.size());

    // En la práctica real: const long long baseCarga = 10000000000LL;
    // Para la demo, reducimos:
    const long long baseCarga = 100000000;  // 100 millones, ajusta si deseas

    for (size_t i = 0; i < threadsTest.size(); i++)
    {
        int nThreads = threadsTest[i];
        long long N = baseCarga * nThreads; // carga proporcional

        omp_set_num_threads(nThreads);
        double start = omp_get_wtime();

        double suma = 0.0;
        #pragma omp parallel for reduction(+:suma)
        for (long long j = 1; j <= N; j++) {
            suma += (j * 1.5) / (j + 1.0);
        }

        double end = omp_get_wtime();
        tiempos[i] = end - start;
    }

    cout << "Tabla de resultados (Ejercicio 5):\n";
    printf("%-10s %-16s %-12s\n", "Hilos", "Elementos proces.", "Tiempo(s)");
    for (size_t i = 0; i < threadsTest.size(); i++)
    {
        long long N = baseCarga * threadsTest[i];
        printf("%-10d %-16lld %-12.4f\n",
               threadsTest[i], N, tiempos[i]);
    }

    cout << "\nAnálisis:\n"
         << "Si la escalabilidad débil fuera perfecta, el tiempo debiera\n"
         << "permanecer aproximadamente constante al duplicar hilos y carga.\n\n";
}


// -----------------------------------------------------------------------------
// MAIN
// -----------------------------------------------------------------------------
int main()
{
    // Ejercicio 1
    //vector<ResultE1> resultadosE1 = runEjercicio1();

    // Ejercicio 2
    //runEjercicio2();

    // Ejercicio 3
    runEjercicio3();

    // Ejercicio 4 (usamos los resultados del Ejercicio 1 para comparar)
    //runEjercicio4(resultadosE1);

    // Ejercicio 5 (opcional)
    //runEjercicio5();

    return 0;
}
