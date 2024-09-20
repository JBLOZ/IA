#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

int main()
{
    pid_t pid_A, pid_B, pid_X, pid_Y, pid_Z;
    pid_A = fork();
    if (pid_A == -1)
    {
        perror("Error en fork");
        exit(-1);
    }
    if (pid_A == 0)
    {
        printf("Soy el proceso A: mi pid es %d. Mi padre es %d\n", getpid(), getppid());
    }
    else
    {
        pid_B = fork();
        if (pid_B == -1)
        {
            perror("Error en fork");
            exit(-1);
        }
        if (pid_B == 0)
            {
            printf("Soy el proceso B: mi pid es %d. Mi padre es %d\n", getpid(), getppid());
            pid_Y = fork();
            }
            if (pid_Y == 0)
                {

                }
                else
                {

                }

            }

    }
    return 0;
}
