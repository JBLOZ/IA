#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <omp.h>
#include <iomanip>
using namespace std;

// Constantes de tamaños de mapa, número de hilos y schedules
const int MAP_SIZES[] = {200, 1000, 2000};
const int NUM_MAPS = 3;
const int THREAD_COUNTS[] = {4, 8, 16};
const int NUM_THREADS = 3;
const string SCHEDULES[] = {"static", "dynamic", "guided"};
const int NUM_SCHEDULES = 3;

const int MIN_FAROLAS = 50, MAX_FAROLAS = 500;
const int BAJO_MIN = 70, BAJO_MAX = 100;
const int MEDIO_MIN = 150, MEDIO_MAX = 200;
const int ALTO_MIN = 250, ALTO_MAX = 300;

struct Celda {
    int num_farolas;
    int consumo_total;
};

void inicializarMapa(vector<vector<Celda>> &mapa, int map_size) {
    // Usamos srand solo una vez; en caso de llamar repetidamente dentro del bucle
    // puede reinicializar la semilla, pero esto es solo un ejemplo.
    srand(time(0));
    for (int i = 0; i < map_size; i++) {
        for (int j = 0; j < map_size; j++) {
            mapa[i][j].num_farolas = rand() % (MAX_FAROLAS - MIN_FAROLAS + 1) + MIN_FAROLAS;
            mapa[i][j].consumo_total = 0;  // reinicializamos para cada celda
            for (int k = 0; k < mapa[i][j].num_farolas; k++) {
                int tipo = rand() % 3;
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

// Función secuencial para calcular totales
void calcularConsumoSecuencial(const vector<vector<Celda>> &mapa, long long &total_farolas, long long &consumo_total, int map_size) {
    total_farolas = 0;
    consumo_total = 0;
    for (int i = 0; i < map_size; i++) {
        for (int j = 0; j < map_size; j++) {
            total_farolas += mapa[i][j].num_farolas;
            consumo_total += mapa[i][j].consumo_total;
        }
    }
}

// Función paralela con schedule(runtime).
// Se utiliza omp_set_schedule() para configurar la política según la cadena recibida.
void calcularConsumoParalelo(const vector<vector<Celda>> &mapa, long long &total_farolas, long long &consumo_total,
                              int map_size, int num_threads, string schedule, double &tiempo) {
    total_farolas = 0;
    consumo_total = 0;
    omp_set_num_threads(num_threads);

    // Configuramos la política de schedule según el parámetro recibido.
    if(schedule == "static")
        omp_set_schedule(omp_sched_static, 0);
    else if(schedule == "dynamic")
        omp_set_schedule(omp_sched_dynamic, 0);
    else if(schedule == "guided")
        omp_set_schedule(omp_sched_guided, 0);

    double start = omp_get_wtime();
    #pragma omp parallel for reduction(+:total_farolas, consumo_total) schedule(runtime)
    for (int i = 0; i < map_size; i++) {
        for (int j = 0; j < map_size; j++) {
            total_farolas += mapa[i][j].num_farolas;
            consumo_total += mapa[i][j].consumo_total;
        }
    }
    tiempo = omp_get_wtime() - start;
}

int main() {
    // Para mostrar resultados con más decimales
    cout << fixed << setprecision(8);

    double totalSecuencialGlobal = 0;
    int countSecuencial = 0;

    // Para acumular promedios por schedule globalmente
    double sumaSchedule[NUM_SCHEDULES] = {0};
    int countSchedule[NUM_SCHEDULES] = {0};

    // Matriz para almacenar el tiempo promedio (sobre schedules) de cada mapa y configuración de hilos.
    double promedioParaleloPorMapa[NUM_MAPS][NUM_THREADS] = {0};

    // Además, para el mensaje final se requiere imprimir “Promedio Paralelo con X hilos MxM”
    // para cada mapa.

    // Recorremos cada tamaño de mapa
    for (int m = 0; m < NUM_MAPS; m++) {
        int map_size = MAP_SIZES[m];
        vector<vector<Celda>> mapa(map_size, vector<Celda>(map_size, {0,0}));
        inicializarMapa(mapa, map_size);

        // Cálculo secuencial (se ejecuta una vez por mapa)
        long long total_farolas_seq, consumo_total_seq;
        double start = omp_get_wtime();
        calcularConsumoSecuencial(mapa, total_farolas_seq, consumo_total_seq, map_size);
        double tiempo_seq = omp_get_wtime() - start;
        totalSecuencialGlobal += tiempo_seq;
        countSecuencial++;

        cout << "\n---------- Mapa tamaño: " << map_size << " ----------\n";
        cout << "Secuencial ->  | Tiempo: " << tiempo_seq << " s" << endl;

        // Variable para acumular, por cada cantidad de hilos, el tiempo (sobre los 3 schedules)
        double sumaTiempoPorThreads[NUM_THREADS] = {0};

        // Recorremos cada schedule y cada configuración de hilos
        for (int s = 0; s < NUM_SCHEDULES; s++) {
            for (int t = 0; t < NUM_THREADS; t++) {
                long long total_farolas_par, consumo_total_par;
                double tiempo_par;
                start = omp_get_wtime();
                calcularConsumoParalelo(mapa, total_farolas_par, consumo_total_par, map_size, THREAD_COUNTS[t], SCHEDULES[s], tiempo_par);
                tiempo_par = omp_get_wtime() - start;
                // Imprimimos cada ejecución paralela (no se vuelcan los totales en cada línea)
                cout << "Paralelo -> Schedule: " << SCHEDULES[s]
                     << " | Hilos: " << THREAD_COUNTS[t]
                     << " ->  | Tiempo: " << tiempo_par << " s" << endl;

                sumaTiempoPorThreads[t] += tiempo_par;

                // Acumulamos para promedios globales por schedule (cada prueba cuenta)
                sumaSchedule[s] += tiempo_par;
                countSchedule[s]++;
            }
        }

        // Imprimimos los resultados numéricos (una sola vez por mapa, según la versión secuencial)
        cout << "Total Farolas: " << total_farolas_seq
             << " | Consumo Total: " << consumo_total_seq << endl;

        cout << "--------------------------------------------\n";

        // Calculamos y guardamos el promedio (sobre los 3 schedules) para cada cantidad de hilos para éste mapa.
        for (int t = 0; t < NUM_THREADS; t++) {
            promedioParaleloPorMapa[m][t] = sumaTiempoPorThreads[t] / NUM_SCHEDULES;
        }
    }

    // Promedio global de la ejecución secuencial
    double promedioSecuencialGlobal = totalSecuencialGlobal / countSecuencial;
    cout << "\nPromedio de ejecución Secuencial: " << promedioSecuencialGlobal << " s\n" << endl;

    // Imprimir promedios paralelos por configuración y por mapa
    for (int m = 0; m < NUM_MAPS; m++) {
        int map_size = MAP_SIZES[m];
        for (int t = 0; t < NUM_THREADS; t++) {
            cout << "Promedio Paralelo con " << THREAD_COUNTS[t] << " hilos "
                 << map_size << "x" << map_size << ": "
                 << promedioParaleloPorMapa[m][t] << " s" << endl;
        }
        cout << endl;
    }

    // Imprimir promedios globales por schedule (a lo largo de todos los mapas y configuraciones)
    for (int s = 0; s < NUM_SCHEDULES; s++) {
        double promSch = sumaSchedule[s] / countSchedule[s];
        cout << "Promedio con schedule " << SCHEDULES[s] << ": " << promSch << " s" << endl;
    }

    return 0;
}
