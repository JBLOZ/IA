FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar la lista de paquetes e instalar sudo, GCC y G++
RUN apt update && \
    apt install -y sudo gcc g++

# Establecer el directorio de trabajo
WORKDIR /home/usuario

# Copiar todos los archivos del directorio actual (donde está el Dockerfile) al directorio de trabajo en el contenedor
COPY . .

# Crear un usuario no root
RUN useradd -ms /bin/bash usuario

# Cambiar al usuario no root
USER usuario

# Comando por defecto
CMD ["/bin/bash"]
