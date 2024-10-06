#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <sys/wait.h>

#define BUFFER_SIZE 1024

// Función para manejar errores de apertura de archivo
void error_al_abrir(const char *archivo)
{
    perror(archivo);
    exit(EXIT_FAILURE);
}

// Función para manejar errores de escritura
void error_al_escribir(const char *mensaje)
{
    perror(mensaje);
    exit(EXIT_FAILURE);
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        fprintf(stderr, "Uso: %s archivo_origen archivo_destino\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char *archivo_origen = argv[1];
    char *archivo_destino = argv[2];

    // Abrir el archivo de origen
    int fd_origen = open(archivo_origen, O_RDONLY);
    if (fd_origen == -1) {error_al_abrir("Error al abrir el archivo origen");}

    // Crear la tubería para la comunicación entre procesos
    int pipe_fd[2];
    if (pipe(pipe_fd) == -1) {perror("Error al crear la tubería");exit(EXIT_FAILURE);}

    pid_t pid = fork();
    if (pid == -1) {perror("Error al hacer fork");exit(EXIT_FAILURE);}


    if (pid == 0)
    {
        // Proceso hijo: lee de la tubería y escribe en el archivo destino
        close(pipe_fd[1]); // Cerrar el extremo de escritura de la tubería

        int fd_destino = open(archivo_destino, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd_destino == -1)
        {
            error_al_abrir("Error al crear el archivo destino");
        }

        char buffer[BUFFER_SIZE];
        ssize_t bytes_leidos;
        while ((bytes_leidos = read(pipe_fd[0], buffer, BUFFER_SIZE)) > 0)
        {
            if (write(fd_destino, buffer, bytes_leidos) == -1)
            {
                error_al_escribir("Error al escribir en el archivo destino");
            }
        }

        if (bytes_leidos == -1)
        {
            perror("Error al leer de la tubería");
            exit(EXIT_FAILURE);
        }

        close(fd_destino);
        close(pipe_fd[0]); // Cerrar el extremo de lectura de la tubería
    }
    if (pid > 0)
    {
      // Proceso padre: lee del archivo origen y escribe en la tubería
      close(pipe_fd[0]); // Cerrar el extremo de lectura de la tubería

      char buffer[BUFFER_SIZE];
      ssize_t bytes_leidos;
      while ((bytes_leidos = read(fd_origen, buffer, BUFFER_SIZE)) > 0)
      {
          if (write(pipe_fd[1], buffer, bytes_leidos) == -1)
          {
              error_al_escribir("Error al escribir en la tubería");
          }
      }

      if (bytes_leidos == -1)
      {
          perror("Error al leer el archivo origen");
          exit(EXIT_FAILURE);
      }

      close(fd_origen);
      close(pipe_fd[1]); // Cerrar el extremo de escritura de la tubería

      wait(NULL); // Esperar a que el proceso hijo termine
  }

    return 0;
}
