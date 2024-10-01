#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

pid_t pid_A, pid_B, pid_X, pid_Y, pid_Z;
pid_t pid_primer_progenitor, pid_segundo_progenitor;
char senyal;

void manejador(int sig)
{
    printf("Senyal %d recibida desde %d\n", sig, getpid());
}

void ls(int sig)
{
    printf("Soy el proceso %c con pid %d, he recibido la señal.\n", senyal, getpid());
    pid_t pid = fork();
    if (pid == 0) {
        // Proceso hijo ejecuta ls y termina
        execlp("ls", "ls", NULL);
        exit(0);
    }
    // El proceso padre continúa sin esperar
}

void pstree(int sig)
{
    printf("Ejecutando 'pstree' en respuesta a la señal %d\n", sig);
    system("pstree -p > salida_pstree.txt");  // Redirige la salida de pstree a un archivo

    // Lee el archivo y muestra su contenido
    FILE *file = fopen("salida_pstree.txt", "r");
    if (file == NULL)
    {
        perror("Error abriendo el archivo de salida de pstree");
        return;
    }

    char linea[256];
    while (fgets(linea, sizeof(linea), file) != NULL)
    {
        printf("%s", linea);  // Imprime cada línea del archivo
    }

    fclose(file);
    remove("salida_pstree.txt");  // Elimina el archivo temporal
}

void terminar_b(int sig)
{
    printf("Soy B (%d) y muero\n", getpid());
    exit(0);
}

int main (int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Error en los argumentos\n");
        exit(EXIT_FAILURE);
    }

    senyal = *argv[1];
    pid_primer_progenitor = getpid();
    printf("Soy el proceso ejec: mi pid es %d\n", pid_primer_progenitor);

    pid_A = fork();
    if (pid_A == -1)
    {
        perror("Error en fork");
        exit(EXIT_FAILURE);
    }

    if (pid_A == 0) // Proceso A
    {
        printf("Soy el proceso A: mi pid es %d. Mi padre es %d\n", getpid(), getppid());
        pid_segundo_progenitor = getpid();

        pid_B = fork();
        if (pid_B == -1)
        {
            perror("Error en fork");
            exit(EXIT_FAILURE);
        }

        if (pid_B == 0) // Proceso B
        {
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_primer_progenitor);

            pid_X = fork();
            if (pid_X == 0) {
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                printf("Soy el proceso X (%d) y muero\n", getpid());
                exit(0);
            }

            pid_Y = fork();
            if (pid_Y == 0) {
                printf("Soy el proceso Y: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                printf("Soy el proceso Y (%d) y muero\n", getpid());
                exit(0);
            }

            pid_Z = fork();
            if (pid_Z == 0) {
                printf("Soy el proceso Z: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                signal(SIGALRM, manejador);
                alarm(atoi(argv[2]));
                pause();
                kill(pid_A, SIGUSR1);
                printf("Soy el proceso Z (%d) y muero\n", getpid());
                exit(0);
            }

            signal(SIGUSR2, terminar_b);
            pause(); // Espera la señal de A para terminar
        }
        else // A
        {
            if (senyal == 'A')
            {
                signal(SIGUSR1, ls);
                pause();
            }

            sleep(1); // Pequeña pausa para asegurar que ls termine
            kill(pid_B, SIGUSR2); // Envía señal a B para que termine
            wait(NULL); // Espera a B
            printf("Soy A (%d) y muero\n", getpid());
            exit(0);
        }
    }
    else // ejec
    {
        wait(NULL); // Espera a A
        printf("Soy ejec (%d) y muero\n", getpid());
    }

    return 0;
}