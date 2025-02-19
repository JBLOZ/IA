#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <omp.h>
#include <string>
using namespace std;

// Rango de valores para la cantidad de farolas y consumo de cada tipo
const int MIN_FAROLAS = 50, MAX_FAROLAS = 500;
const int BAJO_MIN = 70, BAJO_MAX = 100;
const int MEDIO_MIN = 150, MEDIO_MAX = 200;
const int ALTO_MIN = 250, ALTO_MAX = 300;

// Estructura que representa una celda en el mapa
struct Celda {
    int num_farolas;    // Número de farolas en la celda
    int consumo_total;  // Consumo total acumulado en la celda
};

// Función que inicializa el mapa con valores aleatorios para cada celda.
// 'size' es el número de filas y columnas del mapa.
void inicializarMapa(vector<vector<Celda>> &mapa, int size)
{
    srand(time(0));  // Inicializa la semilla para números aleatorios
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            // Asigna un número aleatorio de farolas a la celda
            mapa[i][j].num_farolas = rand() % (MAX_FAROLAS - MIN_FAROLAS + 1) + MIN_FAROLAS;
            // Calcula y suma un consumo aleatorio para cada farola según su tipo
            for (int k = 0; k < mapa[i][j].num_farolas; k++) {
                int tipo = rand() % 3; // Selecciona aleatoriamente un tipo: 0, 1 o 2
                if (tipo == 0)
                    mapa[i][j].consumo_total += rand() % (BAJO_MAX - BAJO_MIN + 1) + BAJO_MIN;
                else if (tipo == 1)
                    mapa[i][j].consumo_total += rand() % (MEDIO_MAX - MEDIO_MIN + 1) + MEDIO_MIN;
                else
                    mapa[i][j].consumo_total += rand() % (ALTO_MAX - ALTO_MIN + 1) + ALTO_MIN;
            }
        }
    }
}

// Función que calcula de forma secuencial el total de farolas y el consumo total del mapa.
void calcularConsumoSecuencial(const vector<vector<Celda>> &mapa, int size, long long &total_farolas, long long &consumo_total)
{
    total_farolas = 0;
    consumo_total = 0;
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            total_farolas += mapa[i][j].num_farolas;
            consumo_total += mapa[i][j].consumo_total;
        }
    }
}

// Función que calcula en paralelo el total de farolas y el consumo total del mapa.
// Se usa 'schedule(runtime)' para que se emplee el schedule configurado en tiempo de ejecución.
void calcularConsumoParalelo(const vector<vector<Celda>> &mapa, int size, long long &total_farolas, long long &consumo_total)
{
    total_farolas = 0;
    consumo_total = 0;
    #pragma omp parallel for reduction(+:total_farolas, consumo_total) schedule(runtime)
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            total_farolas += mapa[i][j].num_farolas;
            consumo_total += mapa[i][j].consumo_total;
        }
    }
}

int main()
{
    // Definición de los tamaños de mapa a probar: 200x200, 1000x1000 y 2000x2000.
    int sizes[] = {200, 1000, 2000};
    // Definición de los tipos de schedule a evaluar.
    string schedules[] = {"static", "dynamic", "guided"};
    // Definición de los números de hilos a usar.
    int thread_counts[] = {4, 8, 16};

    int num_sizes = 3;
    int num_schedules = 3;
    int num_thread_counts = 3;
    // Número de veces que se ejecutará cada experimento paralelo para promediar el tiempo.
    int num_parallel_runs = 3;

    // Para cada tamaño de mapa
    for (int i = 0; i < num_sizes; i++){
        int map_size = sizes[i];

        // --- Ejecución secuencial (se hace una sola vez por tamaño de mapa) ---
        vector<vector<Celda>> mapa_seq(map_size, vector<Celda>(map_size, {0, 0}));
        inicializarMapa(mapa_seq, map_size);
        long long total_farolas_seq, consumo_total_seq;
        double start_seq = omp_get_wtime();
        calcularConsumoSecuencial(mapa_seq, map_size, total_farolas_seq, consumo_total_seq);
        double end_seq = omp_get_wtime();
        double tiempo_seq = end_seq - start_seq;
        cout << "Map Size: " << map_size << "x" << map_size << " - Secuencial:" << endl;
        cout << "Total Farolas: " << total_farolas_seq
             << ", Consumo Total: " << consumo_total_seq
             << ", Tiempo: " << tiempo_seq << " s.\n";
        cout << "----------------------------------------\n";

        // --- Ejecuciones paralelas ---
        for (int s = 0; s < num_schedules; s++){
            for (int t = 0; t < num_thread_counts; t++){
                int current_threads = thread_counts[t];
                // Configura el schedule según el tipo actual
                if (schedules[s] == "static")
                    omp_set_schedule(omp_sched_static, 0);
                else if (schedules[s] == "dynamic")
                    omp_set_schedule(omp_sched_dynamic, 0);
                else if (schedules[s] == "guided")
                    omp_set_schedule(omp_sched_guided, 0);

                // Configura el número de hilos
                omp_set_num_threads(current_threads);

                // Crea e inicializa el mapa para el experimento paralelo.
                vector<vector<Celda>> mapa_par(map_size, vector<Celda>(map_size, {0, 0}));
                inicializarMapa(mapa_par, map_size);

                long long total_farolas_par, consumo_total_par;
                double total_par_time = 0.0;
                // Ejecuta varias veces para obtener el tiempo promedio
                for (int run = 0; run < num_parallel_runs; run++){
                    double start_par = omp_get_wtime();
                    calcularConsumoParalelo(mapa_par, map_size, total_farolas_par, consumo_total_par);
                    double end_par = omp_get_wtime();
                    total_par_time += (end_par - start_par);
                }
                double average_par_time = total_par_time / num_parallel_runs;

                cout << "Map Size: " << map_size << "x" << map_size
                     << ", Schedule: " << schedules[s]
                     << ", Threads: " << current_threads << "\n";
                cout << "Paralelo - Total Farolas: " << total_farolas_par
                     << ", Consumo Total: " << consumo_total_par
                     << ", Tiempo Promedio: " << average_par_time << " s.\n";
                cout << "----------------------------------------\n";
            }
        }
    }

    return 0;
}
