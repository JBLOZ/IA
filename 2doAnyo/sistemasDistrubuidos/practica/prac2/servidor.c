#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>         // close(), fork()
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>     // socket(), bind(), listen(), accept(), send()
#include <netinet/in.h>     // struct sockaddr_in
#include <arpa/inet.h>      // inet_ntoa()
#include <sys/wait.h>       // waitpid()

#define PORT 9999
#define BACKLOG 5          // Tamaño de la cola de conexiones pendientes
#define BUFFER_SIZE 1024   // Tamaño del buffer para enviar datos

int main()
{
    // Declaración de variables
    int socket_fd;                   // Descriptor del socket de escucha
    int new_socket_fd;               // Descriptor del nuevo socket para cada conexión
    struct sockaddr_in server_addr;  // Estructura para la dirección del servidor
    struct sockaddr_in client_addr;  // Estructura para la dirección del cliente
    socklen_t sin_size;              // Tamaño de la estructura de la dirección del cliente
    pid_t pid_child;                 // PID del proceso hijo
    int bind_status;                 // Estado de retorno de bind()
    int listen_status;               // Estado de retorno de listen()
    char buffer[BUFFER_SIZE];        // Buffer para enviar datos
    char *nombre_archivo = "Google.html";  // Nombre del archivo a enviar
    int bytes_read;                  // Número de bytes leídos del archivo
    FILE *archivo_ptr;               // Puntero al archivo

    // Crear el socket
    socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd == -1)
    {
        perror("Error al crear el socket");
        exit(1);
    }

    // Configurar la estructura de la dirección del servidor
    server_addr.sin_family = AF_INET;                 // Usar IPv4
    server_addr.sin_port = htons(PORT);               // Establecer el número de puerto
    server_addr.sin_addr.s_addr = INADDR_ANY;         // Aceptar conexiones desde cualquier IP
    memset(&(server_addr.sin_zero), '\0', 8);         // Poner a cero el resto de la estructura

    // Enlazar el socket a la dirección y puerto
    bind_status = bind(socket_fd, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
    if (bind_status == -1)
    {
        perror("Error en bind");
        close(socket_fd);
        exit(1);
    }

    // Escuchar conexiones entrantes
    listen_status = listen(socket_fd, BACKLOG);
    if (listen_status == -1)
    {
        perror("Error en listen");
        close(socket_fd);
        exit(1);
    }

    printf("Servidor escuchando en el puerto %d...\n", PORT);

    while (1)
    {
        sin_size = sizeof(struct sockaddr_in);
        // Aceptar una conexión entrante
        new_socket_fd = accept(socket_fd, (struct sockaddr *)&client_addr, &sin_size);
        if (new_socket_fd == -1)
        {
            perror("Error en accept");
            continue;
        }

        printf("Conexión aceptada desde %s\n", inet_ntoa(client_addr.sin_addr));

        // Crear un proceso hijo para manejar la conexión
        pid_child = fork();
        if (pid_child == -1)
        {
            perror("Error al hacer fork");
            close(new_socket_fd);
            continue;
        }

        if (pid_child == 0)
        {
            // Proceso hijo
            close(socket_fd);  // El hijo no necesita el socket de escucha

            // Abrir el archivo
            archivo_ptr = fopen(nombre_archivo, "r");
            if (archivo_ptr == NULL)
            {
                fprintf(stderr, "Error al abrir el archivo %s\n", nombre_archivo);
                close(new_socket_fd);
                exit(1);
            }

            // Leer del archivo y enviar al cliente
            while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, archivo_ptr)) > 0)
            {
                if (send(new_socket_fd, buffer, bytes_read, 0) == -1)
                {
                    perror("Error al enviar datos");
                    break;
                }
            }

            fclose(archivo_ptr);
            close(new_socket_fd);
            printf("Archivo enviado correctamente a %s\n", inet_ntoa(client_addr.sin_addr));
            exit(0);
        }
        else
        {
            // Proceso padre
            close(new_socket_fd);  // El padre no necesita este socket
            // Evitar procesos zombis
            waitpid(-1, NULL, WNOHANG);
        }
    }

    // Cerrar el socket de escucha
    close(socket_fd);
    return 0;
}
