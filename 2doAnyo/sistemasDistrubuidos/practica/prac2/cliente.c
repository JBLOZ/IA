#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define PORT 9999
#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s IP_Servidor\n", argv[0]);
        exit(1);
    }

    int sock_fd;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];
    ssize_t bytes;

    // Crear socket
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        perror("socket");
        exit(1);
    }

    // Configurar dirección del servidor

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, argv[1], &server_addr.sin_addr) <= 0) {
        perror("inet_pton");
        close(sock_fd);
        exit(1);
    }

    // Conectar al servidor
    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        close(sock_fd);
        exit(1);
    }

    printf("Conectado al servidor %s en el puerto %d\n", argv[1], PORT);

    // Recibir y mostrar datos
    while ((bytes = recv(sock_fd, buffer, BUFFER_SIZE, 0)) > 0) {
        fwrite(buffer, 1, bytes, stdout);
    }


    printf("\nArchivo recibido correctamente.\n");


    close(sock_fd);
    return 0;
}
