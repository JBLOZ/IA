#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

// Variables globales
pid_t pid_A, pid_B, pid_X, pid_Y, pid_Z;
pid_t pid_ejec_inicial, pid_A_inicial, pid_B_inicial, pid_X_inicial, pid_Y_inicial, pid_Z_inicial;
char senyal;

// Funcion de manejador de señales
void manejador(int sig)
{
    switch (senyal)
    {
        case 'A':
            printf("senyal enviada a %d\n", pid_A_inicial);
            kill(pid_A_inicial, SIGUSR1);
            break;
        case 'B':
            printf("senyal enviada a %d\n", pid_B_inicial);
            kill(pid_B_inicial, SIGUSR1);
            break;
        case 'X':
            printf("senyal enviada a %d\n", pid_X_inicial);
            kill(pid_X_inicial, SIGUSR2);
            break;
        case 'Y':
            printf("senyal enviada a %d\n", pid_Y_inicial);
            kill(pid_Y_inicial, SIGUSR2);
            break;

    }
}

// Funcion para ejecutar ls
void ls(int sig)
{

    pid_t ls = fork();
    if (ls == -1) {perror("Error en fork");exit(1);}
    if (ls == 0)
    {
        printf("ls\n");
        execlp("ls", "ls", NULL);
    }
}

// Funcion para ejecutar pstree
void pstree(int sig)
{

    pid_t pstree = fork();
    if (pstree == -1) {perror("Error en fork");exit(1);}
    if (pstree == 0)
    {
        printf("pstree\n");
        execlp("pstree", "pstree", "-p", NULL);
    }

}

int main (int argc, char *argv[])
{

    // Comprobacion de argumentos
    if (argc != 3)
    {
        printf("Error en los argumentos\n");
        exit(1);
    }
    senyal = *argv[1];
    printf("senyal: %c\n", senyal);


    pid_ejec_inicial = getpid();
    printf("Soy el proceso ejec: mi pid es %d\n", pid_ejec_inicial);

    // Creacion de proceso hijo A
    pid_A = fork();
    if (pid_A == -1){perror("Error en fork");exit(1);}
    if (pid_A == 0)
    {
        pid_A_inicial = getpid();
        printf("Soy el proceso A: mi pid es %d. Mi padre es %d\n", getpid(), getppid());

        // Creacion de proceso hijo B dentro de A
        pid_B = fork();
        if (pid_B == -1) {perror("Error en fork"); exit(1);}
        if (pid_B == 0)
        {
            // Asignacion de pid de B para usarlo luego en el manejador de señales
            pid_B_inicial = getpid();
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pid_ejec_inicial);

            // Creacion de procesos X dentro de B
            pid_X = fork();
            if (pid_X == -1) {perror("Error en fork"); exit(EXIT_FAILURE);}
            if (pid_X == 0)
            {
                pid_X_inicial = getpid();
                signal(SIGUSR2, pstree);
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_A_inicial, pid_ejec_inicial);
                pause(); // pausa obligatoria para que el proceso no muera
                wait(NULL);  // espera a pstree
                printf("Soy X (%d) y muero\n", getpid());
                exit(0);
            }

            // Creacion de procesos Y dentro de B
            pid_Y = fork();
            if (pid_Y == -1) {perror("Error en fork"); exit(EXIT_FAILURE);}
            if (pid_Y == 0)
            {
                pid_Y_inicial = getpid();
                signal(SIGUSR2, pstree);
                printf("Soy el proceso Y: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_A_inicial, pid_ejec_inicial);
                pause(); // pausa obligatoria para que el proceso no muera
                wait(NULL);  // espera a pstree
                printf("Soy Y (%d) y muero\n", getpid());
                exit(0);
            }

            // Creacion de procesos Z dentro de B
            pid_Z = fork();
            if (pid_Z == -1) {perror("Error en fork"); exit(EXIT_FAILURE);}
            if (pid_Z == 0)
            {

                printf("Soy el proceso Z: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n", getpid(), getppid(), pid_A_inicial, pid_ejec_inicial);
                signal(SIGALRM, manejador);
                pid_Y_inicial = (getpid()-1);pid_X_inicial = (getpid()-2);
                alarm(atoi(argv[2]));

                pause();

                // matanzas de procesos despues de realizar las acciones de cada proceso para que mueran X y Y ya que estan esperando indefinidamente
                if (senyal == 'Y') {
                    sleep(1);
                    kill(pid_X_inicial, 9);
                    printf("Soy X (%d) y muero\n", pid_X_inicial);
                }
                if (senyal == 'X') {
                    sleep(1);
                    kill(pid_Y_inicial, 9);
                    printf("Soy Y (%d) y muero\n", pid_Y_inicial);
                }
                if (senyal == 'B' || senyal == 'A') {
                    sleep(1);
                    kill(pid_X_inicial, 9);
                    kill(pid_Y_inicial, 9);
                    printf("Soy X (%d) y muero\n", pid_X_inicial);
                    printf("Soy Y (%d) y muero\n", pid_Y_inicial);
                }
                printf("Soy Z (%d) y muero\n", getpid());
                exit(0);
            }
            // solo B
            signal(SIGUSR1, ls);
            if (senyal == 'B') {pause();}
            wait(NULL);wait(NULL);wait(NULL); wait(NULL);   // B espera a X, Y, Z y ls

            printf("Soy B (%d) y muero\n", getpid());
            exit(0);
        } // solo A

        signal(SIGUSR1, ls);
        if (senyal == 'A') {pause();}
        wait(NULL); wait(NULL); // A espera a B y ls
        printf("Soy A (%d) y muero\n", getpid());
        exit(0);
    } // solo Ejec

    wait(NULL);  // espera a A
    printf("Soy ejec (%d) y muero\n", getpid());
    return 0;

}
