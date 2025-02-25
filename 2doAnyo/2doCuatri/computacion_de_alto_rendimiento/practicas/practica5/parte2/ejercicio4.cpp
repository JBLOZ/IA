#include <stdio.h>
#include <omp.h>

#define PASOS 100 // Se define el número total de pasos en la preparación

int main() {
int plato = 0; // Variable compartida que acumula el total de ingredientes
printf("🍽️ Cocineros colaborando para preparar un plato en %d pasos...\n", PASOS);
// Inicio de la región paralela: aquí se crean múltiples hilos para simular a los cocineros
#pragma omp parallel
{
    int id = omp_get_thread_num();  // Cada hilo obtiene su identificador

    // Distribución de iteraciones del bucle entre hilos para trabajar en paralelo
    #pragma omp for
    for (int i = 0; i < PASOS; i++) {

        // Si el paso actual es 50, se ejecuta la sección especial controlada por el Gran Chef
        if (i == 50) {
            #pragma omp critical  // Sección crítica: solo un hilo puede ejecutar este bloque a la vez
            {
                printf("👨‍🍳 Gran Chef %d está preparando una sección especial...\n", id);
                for (int j = 1; j <= 5; j++) {
                    plato += 1;  // Se añaden 5 ingredientes especiales de forma secuencial
                    printf("👨‍🍳 Gran Chef %d añadió ingrediente especial %d. Total: %d\n", id, j, plato);
                }
            }
        } else {
            // En los demás pasos, se simula la preparación del ingrediente en 3 subpasos
            int preparado = 0;
            for (int k = 0; k < 3; k++) {
                preparado += 1;  // Simula el proceso interno de preparación
            }
            // Se actualiza la variable compartida 'plato' de forma atómica para evitar condiciones de carrera
            #pragma omp atomic
            plato += preparado;
            printf("👨‍🍳 Cocinero %d añadió ingrediente preparado (%d pasos). Total: %d\n", id, preparado, plato);
        }
    } // Fin del for de iteraciones

    // [Opcional] Barrera para sincronizar a todos los hilos: garantiza que todos completen sus tareas antes de terminar la región paralela
    // #pragma omp barrier
} // Fin de la región paralela

// Al terminar la región paralela, se muestra el total de ingredientes añadidos al plato
printf("🍲 Plato terminado con %d ingredientes.\n", plato);
return 0;
}
