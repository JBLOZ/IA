#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

pid_t pid_A, pid_B, pid_X, pid_Y, pid_Z;
pid_t pid_primer_progenitor, pid_segundo_progenitor;
char senyal;

void manejador(int sig)
{
    switch (senyal)
    {
        case 'A':
            printf("senyal enviada a %d\n", pid_A);
            kill(pid_A, SIGUSR1);
            break;
        case 'B':
            printf("senyal enviada a %d\n", pid_B);
            kill(pid_B, SIGUSR1);
            break;
        case 'X':
            printf("senyal enviada a %d\n", pid_X);
            kill(pid_X, SIGUSR2);
            break;
        case 'Y':
            printf("senyal enviada a %d\n", pid_Y);
            kill(pid_Y, SIGUSR2);
            break;

    }
}
void ls(int sig)
{
    pid_t ls = fork();
    if (ls == -1)
    {
        perror("Error en fork");
        exit(EXIT_FAILURE);
    }
    if (ls == 0)
    {
        execlp("ls", "ls", NULL);
    }
}

void pstree(int sig)
{
    pid_t pstree = fork();
    if (pstree == -1)
    {
        perror("Error en fork");
        exit(EXIT_FAILURE);
    }
    if (pstree == 0)
    {
        execlp("pstree", "pstree", "-p", NULL);
    }
}

int main (int argc, char *argv[])
{

    if (argc != 3)
    {
        printf("Error en los argumentos\n");
        exit(EXIT_FAILURE);
    }
    senyal = *argv[1];
    printf("senyal: %c\n", senyal);


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

        pid_segundo_progenitor = getpid();
        printf("Soy el proceso A: mi pid es %d. Mi padre es %d\n", getpid(), getppid());
        signal(SIGUSR1, ls);
        pid_B = fork();

        if (pid_B == -1)
        {
            perror("Error en fork");
            exit(EXIT_FAILURE);
        }

        if (pid_B == 0)
        {

            printf("Soy el proceso B: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_primer_progenitor);

            signal(SIGUSR1, ls);
            pid_X = fork();
            if (pid_X == -1)
            {
                perror("Error en fork");
                exit(EXIT_FAILURE);
            }
            if (pid_X == 0)
            {
                signal(SIGUSR2, pstree);
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
                    signal(SIGUSR2, pstree);
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
                        signal(SIGALRM, manejador);
                        alarm(atoi(argv[2]));
                        pause();


                    }
                    else // b
                    {
                        wait(NULL);
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

        wait(NULL);
        printf("Soy A (%d) y muero\n", getpid());
        }
    }
    else
    {
        wait(NULL);
        printf("Soy ejec (%d) y muero\n", pid_primer_progenitor);
        return 0;
    }
}
