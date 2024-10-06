#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <time.h>

#define NUM_COUNT 10
#define SHM_SIZE sizeof(int) * NUM_COUNT

int main() {
    key_t key = ftok("shmfile", 65); // Crear una clave para la memoria compartida
    int shmid = shmget(key, SHM_SIZE, 0666 | IPC_CREAT); // Crear el segmento de memoria compartida
    if (shmid == -1) {
        perror("Error al crear la memoria compartida");
        exit(EXIT_FAILURE);
    }

    int *nums = (int *)shmat(shmid, NULL, 0); // Adjuntar el segmento de memoria compartida
    if (nums == (int *)-1) {
        perror("Error al adjuntar la memoria compartida");
        exit(EXIT_FAILURE);
    }

    pid_t pid = fork();
    if (pid < 0) {
        perror("Error al hacer fork");
        exit(EXIT_FAILURE);
    } else if (pid == 0) {
        // Proceso hijo: genera los números aleatorios y los escribe en la memoria compartida
        srand(time(NULL));
        printf("Soy el hijo (%d): los números generados son: ", getpid());
        for (int i = 0; i < NUM_COUNT; i++) {
            nums[i] = rand() % 100; // Generar un número aleatorio entre 0 y 99
            printf("%d%s", nums[i], (i == NUM_COUNT - 1) ? "\n" : ", ");
        }
        shmdt(nums); // Desadjuntar la memoria compartida
        exit(EXIT_SUCCESS);
    } else {
        // Proceso padre: espera al hijo y luego lee los números de la memoria compartida
        wait(NULL);
        printf("Soy el padre (%d). Los números generados fueron: ", getpid());
        int suma = 0;
        for (int i = 0; i < NUM_COUNT; i++) {
            printf("%d%s", nums[i], (i == NUM_COUNT - 1) ? "\n" : ", ");
            suma += nums[i];
        }
        float media = suma / (float)NUM_COUNT;
        printf("La media es de %.2f\n", media);

        shmdt(nums); // Desadjuntar la memoria compartida
        shmctl(shmid, IPC_RMID, NULL); // Liberar la memoria compartida
    }

    return 0;
}
