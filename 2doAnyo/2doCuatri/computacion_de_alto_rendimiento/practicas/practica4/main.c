#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <omp.h>
using namespace std;

// Definición de constantes para configurar el tamaño del mapa y los rangos de valores
const int MAP_SIZE = 200;                   // Tamaño del mapa: 200 x 200 celdas
const int MIN_FAROLAS = 50, MAX_FAROLAS = 500; // Rango aleatorio para la cantidad de farolas en cada celda
const int BAJO_MIN = 70, BAJO_MAX = 100;       // Rango de consumo para farolas de tipo bajo
const int MEDIO_MIN = 150, MEDIO_MAX = 200;    // Rango de consumo para farolas de tipo medio
const int ALTO_MIN = 250, ALTO_MAX = 300;      // Rango de consumo para farolas de tipo alto

// Estructura que representa una celda en el mapa
struct Celda {
    int num_farolas;    // Número de farolas en la celda
    int consumo_total;  // Consumo total acumulado de todas las farolas en la celda
};

// Función que inicializa el mapa con valores aleatorios para cada celda
void inicializarMapa(vector<vector<Celda>> &mapa)
{
    srand(time(0));  // Inicializa la semilla para la generación de números aleatorios
    for (int i = 0; i < MAP_SIZE; i++)
    {
        for (int j = 0; j < MAP_SIZE; j++)
        {
            // Asigna un número aleatorio de farolas a la celda
            mapa[i][j].num_farolas = rand() % (MAX_FAROLAS - MIN_FAROLAS + 1) + MIN_FAROLAS;
            // Calcula y suma un consumo aleatorio para cada farola según su tipo
            for (int k = 0; k < mapa[i][j].num_farolas; k++)
            {
                int tipo = rand() % 3; // Selecciona aleatoriamente el tipo de farola
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

// Función que calcula de forma secuencial el total de farolas y el consumo total del mapa
void calcularConsumoSecuencial(const vector<vector<Celda>> &mapa, long long &total_farolas, long long &consumo_total)
{
    total_farolas = 0;
    consumo_total = 0;
    for (int i = 0; i < MAP_SIZE; i++)
    {
        for (int j = 0; j < MAP_SIZE; j++)
        {
            total_farolas += mapa[i][j].num_farolas;
            consumo_total += mapa[i][j].consumo_total;
        }
    }
}

// Función que calcula en paralelo el total de farolas y el consumo total del mapa
void calcularConsumoParalelo(const vector<vector<Celda>> &mapa, long long &total_farolas, long long &consumo_total)
{
    total_farolas = 0;
    consumo_total = 0;
    // Paraleliza el bucle externo con reducción para acumular sumas correctamente
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
    // Crea un mapa de celdas de tamaño MAP_SIZE x MAP_SIZE, inicializado a {0, 0}
    vector<vector<Celda>> mapa(MAP_SIZE, vector<Celda>(MAP_SIZE, {0, 0}));

    // Inicializa el mapa con valores aleatorios
    inicializarMapa(mapa);

    long long total_farolas_seq, consumo_total_seq;
    double start_seq = omp_get_wtime(); // Tiempo de inicio del cálculo secuencial
    calcularConsumoSecuencial(mapa, total_farolas_seq, consumo_total_seq);
    double end_seq = omp_get_wtime(); // Tiempo final del cálculo secuencial
    double tiempo_seq = end_seq - start_seq; // Tiempo transcurrido

    // Imprime los resultados del cálculo secuencial
    cout << "Secuencial - Total Farolas: " << total_farolas_seq
         << ", Consumo Total: " << consumo_total_seq
         << ", Tiempo: " << tiempo_seq << " segundos." << endl;

    long long total_farolas_par, consumo_total_par;
    double start_par = omp_get_wtime(); // Tiempo de inicio del cálculo paralelo
    calcularConsumoParalelo(mapa, total_farolas_par, consumo_total_par);
    double end_par = omp_get_wtime(); // Tiempo final del cálculo paralelo
    double tiempo_par = end_par - start_par; // Tiempo transcurrido

    // Imprime los resultados del cálculo paralelo
    cout << "Paralelo   - Total Farolas: " << total_farolas_par
         << ", Consumo Total: " << consumo_total_par
         << ", Tiempo: " << tiempo_par << " segundos." << endl;

    return 0;
}
