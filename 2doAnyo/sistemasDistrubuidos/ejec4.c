#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/wait.h>
#include <signal.h>
#include <stdlib.h>

struct pids_struct {
    pid_t pid_a;
    pid_t pid_b;
    pid_t pid_x;
    pid_t pid_y;
};

volatile sig_atomic_t signal_received = 0;

void a_handler(int sig) {
    signal_received = 1;
    printf("Soy el proceso A con pid %d, he recibido la señal.\n", getpid());
    execlp("pstree", "pstree", NULL);
    perror("execlp failed");
    exit(1);
}

void b_handler(int sig) {
    signal_received = 1;
    printf("Soy el proceso B con pid %d, he recibido la señal.\n", getpid());
    execlp("pstree", "pstree", NULL);
    perror("execlp failed");
    exit(1);
}

void x_handler(int sig) {
    printf("Soy el proceso X con pid %d, he recibido la señal.\n", getpid());
    execlp("ls", "ls", NULL);
    perror("execlp failed");
    exit(1);
}

void y_handler(int sig) {
    printf("Soy el proceso Y con pid %d, he recibido la señal.\n", getpid());
    execlp("ls", "ls", NULL);
    perror("execlp failed");
    exit(1);
}

void z_handler(int sig) {
    // Do nothing, just wake up from pause
}

int main(int argc, char *argv[]) {
    // Parse arguments
    if (argc != 3) {
        fprintf(stderr, "Usage: %s [A|B|X|Y] N\n", argv[0]);
        exit(1);
    }
    char target_process = argv[1][0];
    int N = atoi(argv[2]);

    // Create shared memory segment
    key_t key = ftok("shmfile", 65);
    int shmid = shmget(key, sizeof(struct pids_struct), 0666|IPC_CREAT);
    struct pids_struct *pids = (struct pids_struct*) shmat(shmid, NULL, 0);

    // Initialize pids to zero
    pids->pid_a = 0;
    pids->pid_b = 0;
    pids->pid_x = 0;
    pids->pid_y = 0;

    printf("Soy el proceso ejec: mi pid es %d\n", getpid());

    pid_t pid_a = fork();
    if (pid_a == -1) { perror("fork failed"); exit(1); }

    if (pid_a == 0) {
        // In process A
        pids->pid_a = getpid();
        printf("Soy el proceso A: mi pid es %d. Mi padre es %d\n", getpid(), getppid());

        // Set up signal handler
        signal(SIGUSR1, a_handler);

        // Fork to create B
        pid_t pid_b = fork();
        if (pid_b == -1) { perror("fork failed"); exit(1); }

        if (pid_b == 0) {
            // In process B
            pids->pid_b = getpid();
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d. Mi abuelo es %d\n", getpid(), getppid(), pids->pid_a);

            // Set up signal handler
            signal(SIGUSR1, b_handler);

            // Fork to create X
            pid_t pid_x = fork();
            if (pid_x == -1) { perror("fork failed"); exit(1); }

            if (pid_x == 0) {
                // In process X
                pids->pid_x = getpid();
                printf("Soy el proceso X: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n",
                    getpid(), getppid(), pids->pid_b, pids->pid_a);
                
                // Set up signal handler
                signal(SIGUSR1, x_handler);

                // Wait for signal
                pause();

                printf("Soy X (%d) y muero\n", getpid());

                exit(0);

            } else {
                // Fork to create Y
                pid_t pid_y = fork();
                if (pid_y == -1) { perror("fork failed"); exit(1); }

                if (pid_y == 0) {
                    // In process Y
                    pids->pid_y = getpid();
                    printf("Soy el proceso Y: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n",
                        getpid(), getppid(), pids->pid_b, pids->pid_a);

                    // Set up signal handler
                    signal(SIGUSR1, y_handler);

                    // Wait for signal
                    pause();

                    printf("Soy Y (%d) y muero\n", getpid());

                    exit(0);
                } else {
                    // Fork to create Z
                    pid_t pid_z = fork();
                    if (pid_z == -1) { perror("fork failed"); exit(1); }

                    if (pid_z == 0) {
                        // In process Z
                        printf("Soy el proceso Z: mi pid es %d. Mi padre es %d. Mi abuelo es %d. Mi bisabuelo es %d\n",
                            getpid(), getppid(), pids->pid_b, pids->pid_a);

                        // Z code
                        // Wait for N seconds without using sleep

                        // Set up signal handler for SIGALRM
                        signal(SIGALRM, z_handler);

                        alarm(N);

                        pause();

                        // After alarm, send signal to target process

                        pid_t target_pid = 0;
                        switch (target_process) {
                            case 'A': target_pid = pids->pid_a; break;
                            case 'B': target_pid = pids->pid_b; break;
                            case 'X': target_pid = pids->pid_x; break;
                            case 'Y': target_pid = pids->pid_y; break;
                            default:
                                fprintf(stderr, "Invalid target process '%c'\n", target_process);
                                exit(1);
                        }
                        if (target_pid == 0) {
                            fprintf(stderr, "Target process pid is 0\n");
                            exit(1);
                        }

                        kill(target_pid, SIGUSR1);

                        printf("Soy Z (%d) y muero\n", getpid());

                        exit(0);
                    } else {
                        // In B, wait for X, Y, Z
                        int status;

                        waitpid(pid_x, &status, 0);
                        waitpid(pid_y, &status, 0);
                        waitpid(pid_z, &status, 0);

                        // Wait for signal if not already received
                        if (!signal_received) {
                            pause();
                        }

                        printf("Soy B (%d) y muero\n", getpid());

                        exit(0);
                    }
                }
            }

        } else {
            // In A, wait for B
            int status;
            waitpid(pid_b, &status, 0);

            // Wait for signal if not already received
            if (!signal_received) {
                pause();
            }

            printf("Soy A (%d) y muero\n", getpid());

            exit(0);
        }

    } else {
        // In ejec, wait for A
        int status;
        waitpid(pid_a, &status, 0);

        // Clean up shared memory
        shmdt(pids);
        shmctl(shmid, IPC_RMID, NULL);

        printf("Soy ejec (%d) y muero\n", getpid());
    }

    return 0;
}

