# Practica 2. Sistenas operativos

**Cod: 33662**
**Jordi Blasco Lozano**

**Practica 2.2**
**TCP/IP.**
**CLIENTE**
**SERVIDOR**

**Jordi Blasco Lozano**

**Sistemas operativos y distribuidos**
**Grado en Inteligencia Artificial**
**Fecha: 21/11/2024**

## Indice

* [Introduccion](#introduccion)
* [Trabajos a realizar](#trabajos-a-realizar)
* [Implementacion del servidor](#implementacion-del-servidor)
 * [Creacion del socket y enlace](#creacion-del-socket-y-enlace)
 * [Escucha y aceptacion de conexiones](#escucha-y-acceptacion-de-conexiones)
 * [Transferencia de archivos](#transferencia-de-archivos)
* [Implementacion del cliente](#implementacion-del-cliente)
 * [Creacion del socket y conexion](#creacion-del-socket-y-conexion)
 * [Recepcion de archivos](#recepcion-de-archivos)
* [Resultados](#resultados)

## Introduccion

En esta practica se ha implementado una aplicacion cliente-servidor utilizando sockets TCP. El objetivo principal es que el servidor transfiera el archivo "Google.html" al cliente, quien posteriormente lo mostrara por pantalla. El servidor se mantiene a la escucha por el puerto 9999, aceptando conexiones y generando un proceso hijo para cada cliente que se conecte.

## Trabajos a realizar

Crear un servidor que pueda recibir conexiones y enviar un archivo al cliente.
Crear un cliente que se conecte al servidor y reciba el archivo.

## Implementacion del servidor

La funcion principal del servidor es escuchar a los clientes y transferirles el archivo.

### Creacion del socket y enlace

Primero, se usa la funcion socket() para crear un socket. Luego se configura la direccion del servidor utilizando la estructura sockaddr_in y se conecta al socket con bind(). Despues, usamos listen() para permitir que el servidor escuche hasta 5 conexiones.

### Escucha y aceptacion de conexiones

Con accept(), el servidor acepta conexiones de los clientes. Cada vez que se acepta una conexion, se crea un proceso hijo usando fork(). El proceso hijo se encarga de enviar el archivo, mientras que el proceso padre sigue esperando nuevas conexiones.

### Transferencia de archivos

El archivo "Google.html" se abre y se lee en partes de tamano BUFFERSIZE que se envian al cliente con send(). Cuando se termina de enviar el archivo, el proceso hijo cierra la conexion.

## Implementacion del cliente

El cliente tiene la funcion de conectarse al servidor, recibir el archivo y posteriormente escribirlo.

### Creacion del socket y conexion

El cliente usa socket() para crear el socket y luego connect() para conectarse al servidor. Para ejecutar el cliente, se necesita especificar la direccion IP del servidor que sera pasada por parametro.

### Recepcion de archivos

Una vez conectado, el cliente recibe el archivo en partes usando recv(). El contenido del archivo se imprime en pantalla para asegurarse de que todo se recibio correctamente.

## Resultados
