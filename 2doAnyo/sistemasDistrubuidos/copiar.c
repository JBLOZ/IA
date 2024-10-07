#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>

#define BUFFER_SIZE 1024 // Definición del tamaño del buffer que se utilizará para leer y escribir los datos

int main(int argc, char *argv[])
{
    // Declaración de variables
    char *archivo_origen, *archivo_destino; // Variables para almacenar los nombres de los archivos
    int fd_origen, fd_destino; // Descriptores de archivo para el archivo de origen y destino
    int pipe_fd[2]; // Array para almacenar los descriptores de los extremos de la tubería: lectura y escritura
    pid_t pid; // Variable para almacenar el identificador del proceso hijo
    char buffer[BUFFER_SIZE]; // Buffer para almacenar los datos que se leerán y escribirán
    ssize_t bytes_leidos; // Variable para almacenar la cantidad de bytes leídos

    // Verificación de argumentos
    if (argc != 3)
    {
        fprintf(stderr, "Uso: %s archivo_origen archivo_destino\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // Asignación de nombres de archivos
    archivo_origen = argv[1];
    archivo_destino = argv[2];

    // Abrir el archivo de origen
    if ((fd_origen = open(archivo_origen, O_RDONLY)) == -1)
    {
        perror("Error al abrir el archivo origen");
        exit(EXIT_FAILURE);
    }

    // Crear la tubería
    if (pipe(pipe_fd) == -1)
    {
        perror("Error al crear la tubería");
        exit(EXIT_FAILURE);
    }

    // Crear el proceso hijo
    pid = fork();
    if (pid == -1)
    {
        perror("Error al hacer fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0)
    {
        // Proceso hijo: lee de la tubería y escribe en el archivo destino
        close(pipe_fd[1]); // Cerrar el extremo de escritura de la tubería, ya que el proceso hijo solo necesita leer.

        // Abrir el archivo de destino
        fd_destino = open(archivo_destino, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd_destino == -1)
        {
            perror("Error al crear el archivo destino");
            exit(EXIT_FAILURE);
        }

        // Leer de la tubería y escribir en el archivo de destino
        while (1)
        {
            bytes_leidos = read(pipe_fd[0], buffer, BUFFER_SIZE);
            if (bytes_leidos == 0) // No hay más datos para leer
            {
                break;
            }
            if (bytes_leidos == -1) // Error al leer de la tubería
            {
                perror("Error al leer de la tubería");
                exit(EXIT_FAILURE);
            }
            if (write(fd_destino, buffer, bytes_leidos) == -1)
            {
                perror("Error al escribir en el archivo destino");
                exit(EXIT_FAILURE);
            }
        }

        // Cerrar el archivo de destino y el extremo de lectura de la tubería
        close(fd_destino);
        close(pipe_fd[0]);
    }
    else
    {
        // Proceso padre: lee del archivo origen y escribe en la tubería
        close(pipe_fd[0]); // Cerrar el extremo de lectura de la tubería, ya que el proceso padre solo necesita escribir.

        // Leer del archivo de origen y escribir en la tubería
        while (1)
        {
            bytes_leidos = read(fd_origen, buffer, BUFFER_SIZE);
            if (bytes_leidos == 0) // No hay más datos para leer
            {
                break;
            }
            if (bytes_leidos == -1) // Error al leer del archivo origen
            {
                perror("Error al leer el archivo origen");
                exit(EXIT_FAILURE);
            }
            if (write(pipe_fd[1], buffer, bytes_leidos) == -1)
            {
                perror("Error al escribir en la tubería");
                exit(EXIT_FAILURE);
            }
        }

        // Cerrar el archivo de origen y el extremo de escritura de la tubería
        close(fd_origen);        
        close(pipe_fd[1]);

        // Esperar a que el proceso hijo termine
        wait(NULL);
    }

    return 0;
}



