#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>
#include <string.h>

pid_t pid_A, pid_B, pid_X, pid_Y, pid_Z;
pid_t pid_primer_progenitor, pid_segundo_progenitor;
char proceso_objetivo;
int tiempo_espera;

void manejador_orden(int sig)
{
    if (sig == SIGUSR1)
    {
        if (proceso_objetivo == 'A' || proceso_objetivo == 'B')
        {
            printf("Soy el proceso %c con pid %d, he recibido la señal.\n", proceso_objetivo, getpid());
            execlp("pstree", "pstree", NULL);
        }
        else if (proceso_objetivo == 'X' || proceso_objetivo == 'Y')
        {
            printf("Soy el proceso %c con pid %d, he recibido la señal.\n", proceso_objetivo, getpid());
            execlp("ls", "ls", "-al", NULL);
        }
    }
}


void manejador_alarma(int sig)
{
    // Este manejador será llamado cuando el temporizador (alarm) expire
    printf("Soy el proceso Z: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
    // Enviar señal al proceso correspondiente
    if (proceso_objetivo == 'A')
    {
        kill(pid_A, SIGUSR1);
    }
    else if (proceso_objetivo == 'B')
    {
        kill(pid_B, SIGUSR1);
    }
    else if (proceso_objetivo == 'X')
    {
        kill(pid_X, SIGUSR1);
    }
    else if (proceso_objetivo == 'Y')
    {
        kill(pid_Y, SIGUSR1);
    }
}

void esperar_procesos(pid_t *pids, int num_pids)
{
    for (int i = 0; i < num_pids; i++)
    {
        waitpid(pids[i], NULL, 0);
    }
}


int main (int argc, char *argv[])
{

    if (argc != 3)
        {
            fprintf(stderr, "Uso: %s <proceso objetivo (A/B/X/Y)> <tiempo en segundos>\n", argv[0]);
            exit(EXIT_FAILURE);
        }

        proceso_objetivo = argv[1][0];  // A, B, X o Y
        tiempo_espera = atoi(argv[2]);

    pid_primer_progenitor = getpid();
    printf("Soy el proceso ejec: mi pid es %d\n", getpid());

    // Crear proceso A
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

        // Crear proceso B
        pid_B = fork();
        if (pid_B == -1)
        {
            perror("Error en fork");
            exit(EXIT_FAILURE);
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
                exit(EXIT_FAILURE);
            }

            // Proceso X
            if (pid_X == 0)
            {
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Y mi bisabuelo es %d\n", getpid(), getppid(),pid_segundo_progenitor, pid_primer_progenitor);
                pause();
            }
            else
            {
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
                    printf("Soy el proceso Y: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Y mi bisabuelo es %d\n", getpid(), getppid(),pid_segundo_progenitor, pid_primer_progenitor);
                    pause();
                }
                else
                {
                    pid_Z = fork();
                    if (pid_Z == -1)
                    {
                        perror("Error en fork");
                        exit(EXIT_FAILURE);
                    }
                    if (pid_Z == 0) {
                        signal(SIGALRM, manejador_alarma);  // Asignar manejador de alarma a Z
                        alarm(tiempo_espera);  // Iniciar temporizador
                        pause();  // Esperar a que la alarma se dispare
                        printf("Soy Z (%d) y muero\n", getpid());
                        kill(pid_Z, 9);
                    }
                    else
                    {
                        // Esperar a que todos los procesos terminen en orden
                        pid_t pids[] = {pid_Z, pid_Y, pid_X, pid_B};
                        esperar_procesos(pids, 4);
                        printf("Soy B (%d) y muero\n", pid_B);
                        kill(pid_B, 9);
                    }
                }
            }
        }
        else
        {
            waitpid(pid_B, NULL, 0);  // Esperar a B
            printf("Soy A (%d) y muero\n", pid_A);
            kill(pid_A, 9);
        }
    }
    else
    {
        waitpid(pid_A, NULL, 0);  // Esperar a A
        printf("Soy ejec (%d) y muero\n", pid_primer_progenitor);
        kill(pid_primer_progenitor, 9);
    }

    return 0;
}
