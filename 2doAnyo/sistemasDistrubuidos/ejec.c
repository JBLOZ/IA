#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

pid_t pid_A, pid_B, pid_X, pid_Y, pid_Z;
pid_t pid_primer_progenitor, pid_segundo_progenitor;
char *proceso_objetivo;

void ejecutar_orden(int signo) {
    if (signo == SIGUSR1) {
        if (strcmp(proceso_objetivo, "A") == 0 || strcmp(proceso_objetivo, "B") == 0) {
            printf("Soy el proceso %s con pid %d, he recibido la señal.\n", proceso_objetivo, getpid());
            system("pstree");
        } else if (strcmp(proceso_objetivo, "X") == 0 || strcmp(proceso_objetivo, "Y") == 0) {
            printf("Soy el proceso %s con pid %d, he recibido la señal.\n", proceso_objetivo, getpid());
            system("ls");
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Uso: %s <proceso> <tiempo>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    proceso_objetivo = argv[1];
    int tiempo = atoi(argv[2]);

    pid_primer_progenitor = getpid();
    printf("Soy el proceso ejec: mi pid es %d\n", pid_primer_progenitor);

    pid_A = fork();
    if (pid_A == -1) {
        perror("Error en fork");
        exit(EXIT_FAILURE);
    }

    if (pid_A == 0) {
        pid_segundo_progenitor = getpid();
        printf("Soy el proceso A: mi pid es %d. Mi padre es %d\n", getpid(), getppid());

        pid_B = fork();
        if (pid_B == -1) {
            perror("Error en fork");
            exit(EXIT_FAILURE);
        }

        if (pid_B == 0) {
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_primer_progenitor);

            pid_X = fork();
            if (pid_X == -1) {
                perror("Error en fork");
                exit(EXIT_FAILURE);
            }

            if (pid_X == 0) {
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                if (strcmp(proceso_objetivo, "X") == 0) {
                    signal(SIGUSR1, ejecutar_orden);  // Asocia la señal a la función
                }
                pause();  // Espera a la señal
            } else {
                pid_Y = fork();
                if (pid_Y == -1) {
                    perror("Error en fork");
                    exit(EXIT_FAILURE);
                }

                if (pid_Y == 0) {
                    printf("Soy el proceso Y: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                    if (strcmp(proceso_objetivo, "Y") == 0) {
                        signal(SIGUSR1, ejecutar_orden);  // Asocia la señal a la función
                    }
                    pause();  // Espera a la señal
                } else {
                    pid_Z = fork();
                    if (pid_Z == -1) {
                        perror("Error en fork");
                        exit(EXIT_FAILURE);
                    }

                    if (pid_Z == 0) {
                        printf("Soy el proceso Z: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                        sleep(tiempo);

                        // Enviar la señal SIGUSR1 al proceso objetivo
                        if (strcmp(proceso_objetivo, "A") == 0) {
                            kill(pid_A, SIGUSR1);
                        } else if (strcmp(proceso_objetivo, "B") == 0) {
                            kill(pid_B, SIGUSR1);
                        } else if (strcmp(proceso_objetivo, "X") == 0) {
                            kill(pid_X, SIGUSR1);
                        } else if (strcmp(proceso_objetivo, "Y") == 0) {
                            kill(pid_Y, SIGUSR1);
                        } else {
                            printf("Proceso objetivo no válido\n");
                        }

                        printf("Soy Z (%d) y muero\n", getpid());
                    } else {
                        if (strcmp(proceso_objetivo, "B") == 0) {
                            signal(SIGUSR1, ejecutar_orden);  // Asocia la señal a la función
                        }
                        wait(NULL);
                        printf("Soy Y (%d) y muero\n", pid_Y);
                        printf("Soy X (%d) y muero\n", pid_X);
                        printf("Soy B (%d) y muero\n", pid_B);
                    }
                }
            }
        } else {
            if (strcmp(proceso_objetivo, "A") == 0) {
                signal(SIGUSR1, ejecutar_orden);  // Asocia la señal a la función
            }
            wait(NULL);
            printf("Soy A (%d) y muero\n", getpid());
        }
    } else {
        wait(NULL);
        printf("Soy ejec (%d) y muero\n", pid_primer_progenitor);
        return 0;
    }
}
