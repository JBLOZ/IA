#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

pid_t pid_A, pid_B, pid_X, pid_Y, pid_Z;
pid_t pid_primer_progenitor, pid_segundo_progenitor;

int main (int argc, char *argv[])
{
    int statusEjec;
    pid_primer_progenitor = getpid();
    printf("Soy el proceso ejec: mi pid es %d\n", pid_primer_progenitor);

    pid_A = fork();
    if (pid_A == -1)
    {
        perror("Error en fork");
        exit(EXIT_FAILURE);
    }
    if (pid_A == 0)
    {
        int statusA;
        pid_segundo_progenitor = getpid();
        printf("Soy el proceso A: mi pid es %d. Mi padre es %d\n", getpid(), getppid());
        pid_B = fork();

        if (pid_B == -1)
        {
            perror("Error en fork");
            exit(EXIT_FAILURE);
        }

        if (pid_B == 0)
        {
            int statusB;
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_primer_progenitor);
            
            pid_X = fork();
            if (pid_X == -1) 
            {
                perror("Error en fork");
                exit(EXIT_FAILURE);
            }
            if (pid_X == 0)
            {
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
            }
            else
            {
                pid_Y = fork();
                if (pid_Y == -1)
                {
                    perror("Error en fork");
                    exit(EXIT_FAILURE);
                }
                if (pid_Y == 0)
                {
                    printf("Soy el proceso Y: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                }
                else
                {
                    pid_Z = fork();
                    if (pid_Z == -1)
                    {
                        perror("Error en fork");
                        exit(EXIT_FAILURE);
                    }
                    if (pid_Z == 0) 
                    {
                        printf("Soy el proceso Z: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                    }
                    else
                    {
                        sleep(atoi(argv[1]));
                        printf("Soy A (%d) y he recibido la señal\n", getppid());
                        wait(&statusB);
                        printf("Soy Z (%d) y muero\n", pid_Z);
                        printf("Soy Y (%d) y muero\n", pid_Y);
                        printf("Soy X (%d) y muero\n", pid_X);
                        printf("Soy B (%d) y muero\n", getpid());
                    }
                }
            }
        }
        else
        {
        wait(&statusA);
        printf("Soy A (%d) y muero\n", getpid());
        }
    }
    else
    {
        wait(&statusEjec);
        printf("Soy ejec (%d) y muero\n", pid_primer_progenitor);
        return 0;
    }
}
