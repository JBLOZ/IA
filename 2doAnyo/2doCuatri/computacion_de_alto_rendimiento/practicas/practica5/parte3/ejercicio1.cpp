#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

#define NUM_USUARIOS 10000 // Número simulado de usuarios a procesar

// Función que simula el análisis de la huella de voz para identificar el idioma.
// Retorna un valor entre 0 y 2, representando: 0 => Español, 1 => Inglés, 2 => Francés.
int analizarHuellaVoz(int id_usuario) {
return id_usuario % 3;
}

// Función que simula la obtención de coordenadas GPS a partir de un id de usuario.
// Se generan valores aleatorios basados en el id para latitud y longitud.
void obtenerCoordenadasGPS(int id_usuario, double *lat, double *lon) {
*lat = (id_usuario % 180) - 90 + ((double) rand() / RAND_MAX);
*lon = (id_usuario % 360) - 180 + ((double) rand() / RAND_MAX);
}

int main() {
// Variable para acumular el total de usuarios identificados.
int totalUsuariosIdentificados = 0;
// Variables separadas para contar la cantidad de usuarios identificados por idioma.
int usuariosEsp = 0;  // Contador para Español
int usuariosIng = 0;  // Contador para Inglés
int usuariosFra = 0;  // Contador para Francés

// Variable para contabilizar actualizaciones en la obtención de coordenadas GPS.
int contadorGPS = 0;

// Variables para medición del tiempo de ejecución.
double inicio, fin;

// Inicializar la semilla para la generación de números aleatorios (para simular el GPS).
srand(time(NULL));

// Se toma el tiempo de inicio.
inicio = omp_get_wtime();

// Región paralela que utilizará reducción para actualizar el contador total de usuarios.
// Se utiliza schedule(dynamic) para balancear la carga de procesamiento en función de la complejidad variable.
#pragma omp parallel reduction(+: totalUsuariosIdentificados)
{
    int id_thread = omp_get_thread_num();
    int idioma_local;
    double lat, lon;

    // Bucle principal que procesa cada usuario en paralelo.
    // Se usa schedule(dynamic) para distribuir la carga de forma dinámica.
    #pragma omp for schedule(dynamic)
    for (int i = 0; i < NUM_USUARIOS; i++) {
        // 1. Identificación de Usuario por Huella de Voz:
        idioma_local = analizarHuellaVoz(i);
        totalUsuariosIdentificados++;  // Se incrementa en forma segura gracias a la reducción.

        // 2. Detección de Idioma:
        // Se actualizan los contadores por idioma. Se emplea #pragma omp atomic para cada actualización simple.
        if (idioma_local == 0) {
            #pragma omp atomic
            usuariosEsp++;
        } else if (idioma_local == 1) {
            #pragma omp atomic
            usuariosIng++;
        } else if (idioma_local == 2) {
            #pragma omp atomic
            usuariosFra++;
        }

        // 3. Geolocalización Global:
        // Se simula la obtención de coordenadas GPS para el usuario y se actualiza el contador correspondiente.
        obtenerCoordenadasGPS(i, &lat, &lon);
        #pragma omp atomic
        contadorGPS++;

        // 4. Adaptación de Idioma:
        // Si el idioma detectado difiere del idioma predominante (se asume que en la región es Español, valor 0),
        // se sugiere una adaptación. La actualización de la salida se protege mediante una sección critical.
        if (idioma_local != 0) {
            #pragma omp critical
            {
                printf("Thread %d sugiere adaptación de idioma para usuario %d.\n", id_thread, i);
            }
        }
    }  // Fin del bucle for

    // 5. Barrera: se sincroniza a los hilos para asegurar que todos hayan completado esta fase antes de continuar.
    #pragma omp barrier
}  // Fin de la región paralela

// Se toma el tiempo de finalización.
fin = omp_get_wtime();

// Cálculo del tiempo total de ejecución.
double tiempo_total = fin - inicio;

// 6. Análisis Estadístico y Comercial:
// Se imprimen los resultados y estadísticas obtenidas.
printf("\n--- Resultados del Sistema ---\n");
printf("Total de usuarios identificados: %d\n", totalUsuariosIdentificados);
printf("Usuarios por idioma: Español = %d, Inglés = %d, Francés = %d\n", usuariosEsp, usuariosIng, usuariosFra);
printf("Total de actualizaciones GPS: %d\n", contadorGPS);
printf("Tiempo total de ejecución: %f segundos\n", tiempo_total);

return 0;
}
