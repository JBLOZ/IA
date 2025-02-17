#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <omp.h>
using namespace std;

const int MAP_SIZE = 200;
const int MIN_FAROLAS = 50, MAX_FAROLAS = 500;
const int BAJO_MIN = 70, BAJO_MAX = 100;
const int MEDIO_MIN = 150, MEDIO_MAX = 200;
const int ALTO_MIN = 250, ALTO_MAX = 300;

struct Celda {
    int num_farolas;
    int consumo_total;
};

void inicializarMapa(vector<vector<Celda>> &mapa)
{
    srand(time(0));  // Inicializa la semilla para la generación de números aleatorios
    for (int i = 0; i < MAP_SIZE; i++)
    {
        for (int j = 0; j < MAP_SIZE; j++)
        {
            // Asigna un número aleatorio de farolas a la celda (entre MIN_FAROLAS y MAX_FAROLAS)
            mapa[i][j].num_farolas = rand() % (MAX_FAROLAS - MIN_FAROLAS + 1) + MIN_FAROLAS;
            // Se asume que consumo_total está inicializado en 0 en cada celda
            for (int k = 0; k < mapa[i][j].num_farolas; k++)
            {
                // Se escoge aleatoriamente un tipo de farola: 0 (bajo), 1 (medio) o 2 (alto)
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

void calcularConsumoSecuencial(const vector<vector<Celda>> &mapa, long long &total_farolas, long long &consumo_total)
{
    total_farolas = 0;
    consumo_total = 0;
    // Recorre cada celda del mapa y suma la cantidad de farolas y el consumo total
    for (int i = 0; i < MAP_SIZE; i++)
    {
        for (int j = 0; j < MAP_SIZE; j++)
        {
            total_farolas += mapa[i][j].num_farolas;
            consumo_total += mapa[i][j].consumo_total;
        }
    }
}

void calcularConsumoParalelo(const vector<vector<Celda>> &mapa, long long &total_farolas, long long &consumo_total)
{
    total_farolas = 0;
    consumo_total = 0;
    // Se utiliza OpenMP para paralelizar el bucle externo.
    // La cláusula 'reduction' se encarga de sumar en paralelo sin problemas de concurrencia.
    #pragma omp parallel for reduction(+:total_farolas, consumo_total) schedule(dynamic)
    for (int i = 0; i < MAP_SIZE; i++)
    {
        for (int j = 0; j < MAP_SIZE; j++)
        {
            total_farolas += mapa[i][j].num_farolas;
            consumo_total += mapa[i][j].consumo_total;
        }
    }
}

int main()
{
    // Se crea un mapa de MAP_SIZE x MAP_SIZE celdas.
    // Se inicializa cada celda con valores {0,0} para evitar basura en consumo_total.
    vector<vector<Celda>> mapa(MAP_SIZE, vector<Celda>(MAP_SIZE, {0, 0}));

    // Inicializa el mapa asignando un número aleatorio de farolas y calculando el consumo en cada celda.
    inicializarMapa(mapa);

    // Medición de tiempo para el cálculo secuencial
    long long total_farolas_seq, consumo_total_seq;
    double start_seq = omp_get_wtime();
    calcularConsumoSecuencial(mapa, total_farolas_seq, consumo_total_seq);
    double end_seq = omp_get_wtime();
    double tiempo_seq = end_seq - start_seq;

    cout << "Secuencial - Total Farolas: " << total_farolas_seq
         << ", Consumo Total: " << consumo_total_seq
         << ", Tiempo: " << tiempo_seq << " segundos." << endl;

    // Medición de tiempo para el cálculo paralelo
    long long total_farolas_par, consumo_total_par;
    double start_par = omp_get_wtime();
    calcularConsumoParalelo(mapa, total_farolas_par, consumo_total_par);
    double end_par = omp_get_wtime();
    double tiempo_par = end_par - start_par;

    cout << "Paralelo   - Total Farolas: " << total_farolas_par
         << ", Consumo Total: " << consumo_total_par
         << ", Tiempo: " << tiempo_par << " segundos." << endl;

    return 0;
}
