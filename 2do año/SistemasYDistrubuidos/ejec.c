#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

int main()
{
    pid_t pid_A, pid_B, pid_X, pid_Y;
    pid_t pid_primer_progenitor, pid_segundo_progenitor;

    pid_primer_progenitor = getpid();
    printf("Soy el proceso ejec: mi pid es %d\n", getpid());

    // Crear proceso A
    pid_A = fork();
    if (pid_A == -1)
    {
        perror("Error en fork");
        exit(-1);
    }

    // Proceso A
    if (pid_A == 0)
    {
        pid_segundo_progenitor = getpid();
        printf("Soy el proceso A: mi pid es %d. Mi padre es %d\n", getpid(), getppid());

        // Crear proceso B
        pid_B = fork();
        if (pid_B == -1)
        {
            perror("Error en fork");
            exit(-1);
        }

        // Proceso B
        if (pid_B == 0)
        {
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_primer_progenitor);

            // Crear proceso X
            pid_X = fork();
            if (pid_X == -1)
            {
                perror("Error en fork");
                exit(-1);
            }

            // Proceso X
            if (pid_X == 0)
            {
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Y mi bisabuelo es %d\n", getpid(), getppid(),pid_segundo_progenitor, pid_primer_progenitor);
            }
            else
            {
                // Crear proceso Y
                pid_Y = fork();
                if (pid_Y == -1)
                {
                    perror("Error en fork");
                    exit(-1);
                }

                // Proceso Y
                if (pid_Y == 0)
                {
                    printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Y mi bisabuelo es %d\n", getpid(), getppid(),pid_segundo_progenitor, pid_primer_progenitor);

                }
                else
                {
                    // Esperar a que los procesos X e Y terminen
                    wait(NULL);
                    wait(NULL);
                }
            }
        }
        else
        {
            // Esperar a que el proceso B termine
            wait(NULL);
        }
    }
    else
    {
        // Esperar a que el proceso A termine
        wait(NULL);
    }

    return 0;
}
