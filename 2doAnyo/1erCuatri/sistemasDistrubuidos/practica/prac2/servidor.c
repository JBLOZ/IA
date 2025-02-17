#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/wait.h>

#define PORT 9999
#define BACKLOG 5
#define BUFFER_SIZE 1024
#define FILE_NAME "Google.html"

int main() {
    int listen_fd, conn_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    pid_t pid;

    // Crear socket
    listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd < 0) {
        perror("socket");
        exit(1);
    }

    // Configurar dirección del servidor

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    // Enlazar socket
    if (bind(listen_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind");
        close(listen_fd);
        exit(1);
    }

    // Escuchar conexiones
    if (listen(listen_fd, BACKLOG) < 0) {
        perror("listen");
        close(listen_fd);
        exit(1);
    }

    printf("Servidor escuchando en el puerto %d...\n", PORT);

    while (1) {
        // Aceptar una conexión entrante
        conn_fd = accept(listen_fd, (struct sockaddr *)&client_addr, &addr_len);
        if (conn_fd < 0) {
            perror("accept");
            continue;
        }

        printf("Conexión aceptada desde %s\n", inet_ntoa(client_addr.sin_addr));

        // Crear un proceso hijo para manejar la conexión
        pid = fork();
        if (pid < 0) {
            perror("fork");
            close(conn_fd);
            continue;
        }

        if (pid == 0) {
            // Proceso hijo
            close(listen_fd); // El hijo no necesita el socket de escucha

            FILE *file = fopen(FILE_NAME, "r");
            if (!file) {
                perror("fopen");
                close(conn_fd);
                exit(1);
            }

            // Leer del archivo y enviar al cliente
            ssize_t bytes;
            while ((bytes = fread(buffer, 1, BUFFER_SIZE, file)) > 0) {
                if (send(conn_fd, buffer, bytes, 0) < 0) {
                    perror("send");
                    break;
                }
            }

            fclose(file);
            close(conn_fd);
            printf("Archivo enviado correctamente a %s\n", inet_ntoa(client_addr.sin_addr));
            exit(0);
        }

        // Proceso padre
        close(conn_fd); // El padre no necesita este socket
        waitpid(-1, NULL, WNOHANG); // Evitar procesos zombis
    }

    close(listen_fd);
    return 0;
}
