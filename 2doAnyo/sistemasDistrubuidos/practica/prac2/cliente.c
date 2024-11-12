#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>         // close()
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>     // socket(), connect(), recv()
#include <netinet/in.h>     // struct sockaddr_in
#include <arpa/inet.h>      // inet_addr()

#define PORT 9999
#define BUFFER_SIZE 1024  // Tamaño del buffer para recibir datos

int main(int argc, char *argv[])
{
    // Declaración de variables
    int socket_fd;                    // Descriptor del socket
    struct sockaddr_in server_addr;   // Estructura para la dirección del servidor
    int connect_status;               // Estado de retorno de connect()
    char buffer[BUFFER_SIZE];         // Buffer para recibir datos
    int bytes_received;               // Número de bytes recibidos
    char *server_ip;                  // Dirección IP del servidor

    // Verificar los argumentos de línea de comandos
    if (argc != 2)
    {
        fprintf(stderr, "Uso: %s IP_Servidor\n", argv[0]);
        exit(1);
    }

    server_ip = argv[1];

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
    server_addr.sin_addr.s_addr = inet_addr(server_ip);  // Establecer la dirección IP del servidor
    memset(&(server_addr.sin_zero), '\0', 8);         // Poner a cero el resto de la estructura

    // Conectarse al servidor
    connect_status = connect(socket_fd, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
    if (connect_status == -1)
    {
        perror("Error en connect");
        close(socket_fd);
        exit(1);
    }

    printf("Conectado al servidor %s en el puerto %d\n", server_ip, PORT);

    // Recibir datos del servidor
    while ((bytes_received = recv(socket_fd, buffer, BUFFER_SIZE - 1, 0)) > 0)
    {
        buffer[bytes_received] = '\0';  // Asegurar que el buffer es una cadena válida
        printf("%s", buffer);           // Mostrar el contenido recibido
    }

    if (bytes_received == -1)
    {
        perror("Error en recv");
    }
    else
    {
        printf("\nArchivo recibido correctamente.\n");
    }

    // Cerrar el socket
    close(socket_fd);
    return 0;
}
