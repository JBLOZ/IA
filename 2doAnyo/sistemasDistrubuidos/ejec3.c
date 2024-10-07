#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <fcntl.h>
#include <sys/types.h>
#include <time.h>

int main()
{
    int num_count = 10; // Número de elementos a generar
    int shm_size = sizeof(int) * num_count; // Tamaño de la memoria compartida
    // Declaración de variables al inicio
    key_t key; // Clave para la memoria compartida
    int shmid; // ID del segmento de memoria compartida
    int *nums; // Puntero para la memoria compartida
    pid_t pid; // ID del proceso
    float suma = 0; // Variable para almacenar la suma de los números, inicializado como flotante
    float media; // Variable para almacenar la media de los números, resultado será un valor flotante

    // Crear un archivo para ftok si no existe
    int fd = open("shmfile", O_CREAT | O_RDWR, 0666);
    if (fd == -1)
    {
        perror("Error al abrir shmfile");
        exit(EXIT_FAILURE);
    }
    close(fd);

    // Crear una clave para la memoria compartida
    key = ftok("shmfile", 65);
    if (key == -1)
    {
        perror("Error al crear la clave para la memoria compartida");
        exit(EXIT_FAILURE);
    }

    // Crear el segmento de memoria compartida
    shmid = shmget(key, shm_size, 0666 | IPC_CREAT);
    if (shmid == -1)
    {
        perror("Error al crear la memoria compartida");
        exit(EXIT_FAILURE);
    }

    // Adjuntar el segmento de memoria compartida
    nums = (int *)shmat(shmid, NULL, 0);
    if (nums == (int *)-1)
    {
        perror("Error al adjuntar la memoria compartida");
        exit(EXIT_FAILURE);
    }

    // Crear el proceso hijo
    pid = fork();
    if (pid == -1)
    {
        perror("Error al hacer fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0)
    {
        // Proceso hijo: genera los números aleatorios y los escribe en la memoria compartida
        srand(time(NULL) ^ getpid());
        printf("Soy el hijo (%d): los números generados son: ", getpid());
        for (int i = 0; i < num_count; i++)
        {
            nums[i] = rand() % 100; // Generar un número aleatorio entre 0 y 99
            printf("%d%s", nums[i], (i == num_count - 1) ? "\n" : ", ");
        }
        // Desadjuntar la memoria compartida
        if (shmdt(nums) == -1)
        {
            perror("Error al desadjuntar la memoria compartida (hijo)");
            exit(EXIT_FAILURE);
        }
        exit(EXIT_SUCCESS);
    }

    // Proceso padre: espera al hijo y luego lee los números de la memoria compartida
    if (waitpid(pid, NULL, 0) == -1)
    {
        perror("Error al esperar al proceso hijo");
        exit(EXIT_FAILURE);
    }
    printf("Soy el padre (%d). Los números generados fueron: ", getpid());
    for (int i = 0; i < num_count; i++)
    {
        printf("%d%s", nums[i], (i == num_count - 1) ? "\n" : ", ");
        suma += nums[i];
    }
    media = suma / num_count;
    printf("La media es de %.2f\n", media);

    // Desadjuntar y liberar la memoria compartida
    if (shmdt(nums) == -1)
    {
        perror("Error al desadjuntar la memoria compartida (padre)");
        exit(EXIT_FAILURE);
    }
    if (shmctl(shmid, IPC_RMID, NULL) == -1)
    {
        perror("Error al liberar la memoria compartida");
        exit(EXIT_FAILURE);
    }

    return 0;
}
