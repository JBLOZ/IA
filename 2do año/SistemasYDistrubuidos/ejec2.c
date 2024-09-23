#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>
#include <string.h>

// Variables globales
pid_t pid_A, pid_B, pid_X, pid_Y, pid_Z;
pid_t pid_primer_progenitor, pid_segundo_progenitor;
char proceso_objetivo;
int tiempo_espera;

// Manejadores de señales
void manejador_orden(int sig) {
    if (sig == SIGUSR1) {
        if (proceso_objetivo == 'A' || proceso_objetivo == 'B') {
            printf("Soy el proceso %c con pid %d, he recibido la señal.\n", proceso_objetivo, getpid());
            pid_t pid = fork();
            printf("%d", pid);

            if (pid == 0) {
                execlp("pstree", "pstree", NULL);  // Ejecutar pstree
                perror("Error ejecutando pstree");  // Si execlp falla
                exit(EXIT_FAILURE);
            } else {
                waitpid(pid, NULL, 0);  // Esperar a que el comando termine
                exit(EXIT_SUCCESS);  // Terminar el proceso después de ejecutar el comando
            }
        } else if (proceso_objetivo == 'X' || proceso_objetivo == 'Y') {
            printf("Soy el proceso %c con pid %d, he recibido la señal.\n", proceso_objetivo, getpid());
            pid_t pid = fork();
            if (pid == 0) {
                execlp("ls", "ls", NULL);  // Ejecutar ls
                perror("Error ejecutando ls");  // Si execlp falla
                exit(EXIT_FAILURE);
            } else {
                waitpid(pid, NULL, 0);  // Esperar a que el comando termine
                exit(EXIT_SUCCESS);  // Terminar el proceso después de ejecutar el comando
            }
        }
    }
}

void manejador_alarma(int sig) {
    // Este manejador será llamado cuando el temporizador (alarm) expire
    printf("Soy el proceso Z: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
    // Enviar señal al proceso correspondiente
    if (proceso_objetivo == 'A') {
        kill(pid_A, SIGUSR1);
    } else if (proceso_objetivo == 'B') {
        kill(pid_B, SIGUSR1);
    } else if (proceso_objetivo == 'X') {
        kill(pid_X, SIGUSR1);
    } else if (proceso_objetivo == 'Y') {
        kill(pid_Y, SIGUSR1);
    }
}

void esperar_procesos(pid_t *pids, int num_pids) {
    for (int i = 0; i < num_pids; i++) {
        waitpid(pids[i], NULL, 0);
    }
}

int main (int argc, char *argv[]) {
    // Validación de argumentos
    if (argc != 3) {
        fprintf(stderr, "Uso: %s <proceso objetivo (A/B/X/Y)> <tiempo en segundos>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    proceso_objetivo = argv[1][0];  // A, B, X o Y
    tiempo_espera = atoi(argv[2]);  // Tiempo en segundos

    pid_primer_progenitor = getpid();
    printf("Soy el proceso ejec: mi pid es %d\n", pid_primer_progenitor);

    // Crear proceso A
    pid_A = fork();
    if (pid_A == -1) {
        perror("Error en fork");
        exit(EXIT_FAILURE);
    }

    // Proceso A
    if (pid_A == 0) {
        signal(SIGUSR1, manejador_orden);  // Asignar manejador de señal a A
        pid_segundo_progenitor = getpid();
        printf("Soy el proceso A: mi pid es %d. Mi padre es %d\n", getpid(), getppid());

        // Crear proceso B
        pid_B = fork();
        if (pid_B == -1) {
            perror("Error en fork");
            exit(EXIT_FAILURE);
        }

        // Proceso B
        if (pid_B == 0) {
            signal(SIGUSR1, manejador_orden);  // Asignar manejador de señal a B
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_primer_progenitor);

            // Crear proceso X
            pid_X = fork();
            if (pid_X == -1) {
                perror("Error en fork");
                exit(EXIT_FAILURE);
            }

            // Proceso X
            if (pid_X == 0) {
                signal(SIGUSR1, manejador_orden);  // Asignar manejador de señal a X
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                pause();  // Esperar la señal
                exit(EXIT_SUCCESS);
            } else {
                // Crear proceso Y
                pid_Y = fork();
                if (pid_Y == -1) {
                    perror("Error en fork");
                    exit(EXIT_FAILURE);
                }

                // Proceso Y
                if (pid_Y == 0) {
                    signal(SIGUSR1, manejador_orden);  // Asignar manejador de señal a Y
                    printf("Soy el proceso Y: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor, pid_primer_progenitor);
                    pause();  // Esperar la señal
                    exit(EXIT_SUCCESS);
                } else {
                    // Crear proceso Z
                    pid_Z = fork();
                    if (pid_Z == -1) {
                        perror("Error en fork");
                        exit(EXIT_FAILURE);
                    }

                    if (pid_Z == 0) {
                        signal(SIGALRM, manejador_alarma);  // Asignar manejador de alarma a Z
                        alarm(tiempo_espera);  // Iniciar temporizador
                        pause();  // Esperar a que la alarma se dispare
                        printf("Soy Z (%d) y muero\n", getpid());
                        exit(EXIT_SUCCESS);
                    } else {
                        // Esperar a que todos los procesos terminen en orden
                        pid_t pids[] = {pid_Z, pid_Y, pid_X, pid_B};
                        esperar_procesos(pids, 4);
                        printf("Soy B (%d) y muero\n", pid_B);
                        exit(EXIT_SUCCESS);
                    }
                }
            }
        } else {
            waitpid(pid_B, NULL, 0);  // Esperar a B
            printf("Soy A (%d) y muero\n", pid_A);
            exit(EXIT_SUCCESS);
        }
    } else {
        waitpid(pid_A, NULL, 0);  // Esperar a A
        printf("Soy ejec (%d) y muero\n", pid_primer_progenitor);
    }

    return 0;
}
