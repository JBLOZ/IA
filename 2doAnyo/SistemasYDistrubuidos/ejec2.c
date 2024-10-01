#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>


pid_t pid_A, pid_B, pid_X, pid_Y, pid_Z;
pid_t pid_primer_progenitor, pid_segundo_progenitor;

int main () 
{
    pid_primer_progenitor = getpid();
    printf("Soy el proceso ejec: mi pid es %d\n", pid_primer_progenitor);
    
    pid_A = fork();

    if (pid_A == -1) 
    {
        perror("Error en fork");
        exit(EXIT_FAILURE);
    }

    // Proceso A
    if (pid_A == 0) 
    {
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
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_primer_progenitor);
            
            // Crear proceso X
            pid_X = fork();

            if (pid_X == -1) 
            {
                perror("Error en fork");
                exit(EXIT_FAILURE);
            }

            // Proceso X
            if (pid_X == 0) 
            {
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                exit(0);
            }
            
            // Crear proceso Y
            pid_Y = fork();

            if (pid_Y == -1) 
            {
                perror("Error en fork");
                exit(EXIT_FAILURE);
            }

            // Proceso Y
            if (pid_Y == 0) 
            {
                printf("Soy el proceso Y: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                exit(0);
            }

            // Crear proceso Z
            pid_Z = fork();

            if (pid_Z == -1) 
            {
                perror("Error en fork");
                exit(EXIT_FAILURE);
            }

            if (pid_Z == 0) 
            {
                printf("Soy el proceso Z: mi pid es %d y estoy matando a X (%d)\n", getpid(), pid_X);
                kill(pid_X, SIGKILL);  // Matar al proceso X
                exit(0);
            }

            // Esperar a los procesos X, Y, Z
            wait(NULL);  // Espera por Z
            wait(NULL);  // Espera por Y
            wait(NULL);  // Espera por X

            printf("Soy B (%d) y he terminado\n", getpid());
            exit(0);
        }

        // Esperar a que B termine
        wait(NULL);
        printf("Soy A (%d) y he terminado\n", getpid());
        exit(0);
    }

    // Esperar a que A termine
    wait(NULL);
    printf("Soy ejec (%d) y he terminado\n", getpid());

    return 0;
}
