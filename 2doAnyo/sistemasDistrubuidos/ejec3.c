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
    printf("Señal %d recibida desde %d\n", sig, getpid());
}

void ls(int sig)
{
    printf("Ejecutando 'ls' en respuesta a la señal %d\n", sig);
    system("ls > salida_ls.txt");  // Redirige la salida de ls a un archivo

    // Lee el archivo y muestra su contenido en una sola línea
    FILE *file = fopen("salida_ls.txt", "r");
    if (file == NULL)
    {
        perror("Error abriendo el archivo de salida de ls");
        return;
    }

    char linea[256];
    while (fgets(linea, sizeof(linea), file) != NULL)
    {
        linea[strcspn(linea, "\n")] = '\0';  // Elimina el salto de línea
        printf("%s  ", linea);  // Imprime el contenido con dos espacios
    }

    printf("\n");  // Nueva línea al final
    fclose(file);
    remove("salida_ls.txt");  // Elimina el archivo temporal
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
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d\n", getpid(), getppid());

            pid_X = fork();
            if (pid_X == -1)
            {
                perror("Error en fork");
                exit(EXIT_FAILURE);
            }
            if (pid_X == 0) // Proceso X
            {
                signal(SIGUSR2, pstree);
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor);
                pause();
                exit(0);
            }
            else
            {
                pid_Y = fork();
                if (pid_Y == -1)
                {
                    perror("Error en fork");
                    exit(EXIT_FAILURE);
                }
                if (pid_Y == 0) // Proceso Y
                {
                    signal(SIGUSR2, pstree);
                    printf("Soy el proceso Y: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor);
                    pause();
                    exit(0);
                }
                else
                {
                    pid_Z = fork();
                    if (pid_Z == -1)
                    {
                        perror("Error en fork");
                        exit(EXIT_FAILURE);
                    }
                    if (pid_Z == 0) // Proceso Z
                    {
                        signal(SIGALRM, manejador);
                        alarm(atoi(argv[2]));
                        printf("Soy el proceso Z: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_segundo_progenitor);
                        pause();

                        // Enviar señal según el argumento
                        switch (senyal)
                        {
                            case 'A':
                                kill(pid_A, SIGUSR1);
                                break;
                            case 'B':
                                kill(pid_B, SIGUSR1);
                                break;
                            case 'X':
                                kill(pid_X, SIGUSR2);
                                break;
                            case 'Y':
                                kill(pid_Y, SIGUSR2);
                                break;
                            default:
                                break;
                        }
                        exit(0);
                    }
                    else
                    {
                        // Esperar a que Z termine
                        waitpid(pid_Z, NULL, 0);
                        printf("Soy Z (%d) y muero\n", pid_Z);
                    }
                }
                // Esperar a que X e Y terminen
                waitpid(pid_X, NULL, 0);
                printf("Soy X (%d) y muero\n", pid_X);
                waitpid(pid_Y, NULL, 0);
                printf("Soy Y (%d) y muero\n", pid_Y);
            }
            // Esperar a que B termine
            signal(SIGUSR1, ls);
            pause();
            exit(0);
        }
        else
        {
            waitpid(pid_B, NULL, 0);
            printf("Soy B (%d) y muero\n", pid_B);
            signal(SIGUSR1, ls);
            pause();
            exit(0);
        }
    }
    else
    {
        // Espera a A y sus hijos
        waitpid(pid_A, NULL, 0);
        printf("Soy A (%d) y muero\n", pid_A);
    }

    printf("Soy ejec (%d) y muero\n", getpid());
    return 0;
}
