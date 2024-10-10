#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>

 
int main(int argc, char *argv[])
{   int BUFFER_SIZE = 1024;
    // Declaración de variables
    char *archivo_origen, *archivo_destino; // Variables para almacenar los nombres de los archivos
    int d_origen, d_destino; // Descriptores de archivo para el archivo de origen y destino
    int pipe_l_e[2]; // Array para almacenar los descriptores de los extremos de la tubería: lectura y escritura
    pid_t pid_hijo, pid_pipe, pid_write_destino, pid_write_pipe; // Variable para almacenar el identificador del proceso hijo y los valores de retorno de las funciones write y pipe
    char buffer[BUFFER_SIZE]; // Buffer para almacenar los datos que se leerán y escribirán
    ssize_t bytes_leidos; // Variable para almacenar la cantidad de bytes leídos

    // Verificación de argumentos
    if (argc != 3)
    {
        fprintf(stderr, "Uso: %s archivo_origen archivo_destino\n", argv[0]);
        exit(1);
    }

    // Asignación de nombres de archivos
    archivo_origen = argv[1];
    archivo_destino = argv[2];

    // Abrir el archivo de origen
    d_origen = open(archivo_origen, O_RDONLY);
    if (d_origen == -1) { perror("Error al abrir el archivo origen"); exit(1); }

    // Crear la tubería
    pid_pipe = pipe(pipe_l_e); 
    if (pid_pipe == -1) { perror("Error al crear la tubería"); exit(1); }

    // Crear el proceso hijo
    pid_hijo = fork();
    if (pid_hijo == -1) { perror("Error al hacer fork"); exit(1); }
    if (pid_hijo == 0)
    {
        // Proceso hijo: lee de la tubería y escribe en el archivo destino
        close(pipe_l_e[1]); // Cerrar el extremo de escritura de la tubería, ya que el proceso hijo solo necesita leer. 

        // Abrir el archivo de destino
        d_destino = open(archivo_destino, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (d_destino == -1) { perror("Error al crear el archivo destino"); exit(1); }

        // Leer de la tubería y escribir en el archivo destino
        while (1)
        {
            bytes_leidos = read(pipe_l_e[0], buffer, BUFFER_SIZE);
            if (bytes_leidos == 0) // No hay más datos para leer
            {
                break;
            }
            if (bytes_leidos == -1) {perror("Error al leer de la tubería"); exit(1);}

            pid_write_destino = write(d_destino, buffer, bytes_leidos);
            if (pid_write_destino == -1) { perror("Error al escribir en el archivo destino");exit(1);}
        }

        close(d_destino);
        close(pipe_l_e[0]);
        exit(0); 
    }
    // Código del proceso padre
    // Proceso padre: lee del archivo de origen y escribe en la tubería
    close(pipe_l_e[0]); // Cerrar el extremo de lectura de la tubería, ya que el proceso padre solo necesita escribir.

    // Leer del archivo de origen y escribir en la tubería
    while (1)
        {
            bytes_leidos = read(d_origen, buffer, BUFFER_SIZE);
            if (bytes_leidos == 0) 
            {
                break;
            }
            if (bytes_leidos == -1) {perror("Error al leer el archivo origen");exit(1);}

            pid_write_pipe = write(pipe_l_e[1], buffer, bytes_leidos);
            if (pid_write_pipe == -1){perror("Error al escribir en la tubería");exit(1);}
        }

    close(d_origen);
    close(pipe_l_e[1]);

    // Esperar a que el proceso hijo termine
    wait(NULL);
    exit(0);
}