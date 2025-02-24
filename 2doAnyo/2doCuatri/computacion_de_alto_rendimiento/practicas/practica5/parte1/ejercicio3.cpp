#include <iostream>
#include <omp.h>

int main() {
    const int array_size = 100;
    int arr[array_size];

    // Inicializar el array a -1 para identificar fácilmente errores
    for (int i = 0; i < array_size; i++) {
        arr[i] = -1;
    }

    // Región paralela: cada hilo actualiza una porción no solapada del array
    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        int num_threads = omp_get_num_threads();

        // Calcular el tamaño del segmento asignado a cada hilo
        int segment_size = array_size / num_threads;
        int start = thread_id * segment_size;
        // El último hilo se encarga de los elementos restantes, si existen
        int end = (thread_id == num_threads - 1) ? array_size : start + segment_size;

        // Cada hilo escribe su identificador en su segmento del array
        for (int i = start; i < end; i++) {
            arr[i] = thread_id;
        }

        // Barrera: esperar a que todos los hilos hayan completado la escritura
        #pragma omp barrier

        // (Opcional) Cada hilo puede imprimir qué segmento escribió
        #pragma omp critical
        {
            std::cout << "El hilo " << thread_id
                      << " ha escrito desde el índice " << start
                      << " hasta " << end - 1 << std::endl;
        }
    }

    // Verificar fuera de la región paralela que los datos han sido escritos correctamente
    bool correcto = true;
    int num_threads = omp_get_max_threads();
    int segment_size = array_size / num_threads;
    for (int t = 0; t < num_threads; t++) {
        int expected_value = t;
        int start = t * segment_size;
        int end = (t == num_threads - 1) ? array_size : start + segment_size;
        for (int i = start; i < end; i++) {
            if (arr[i] != expected_value) {
                std::cout << "Error en el índice " << i
                          << ". Valor encontrado: " << arr[i]
                          << ", se esperaba: " << expected_value << std::endl;
                correcto = false;
            }
        }
    }

    if (correcto) {
        std::cout << "\nTodos los datos fueron escritos correctamente sin sobrescrituras." << std::endl;
    } else {
        std::cout << "\nSe detectaron errores en la escritura del array." << std::endl;
    }

    return 0;
}
