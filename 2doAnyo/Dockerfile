FROM python:3.10-bullseye
WORKDIR /workdir

# Copiamos el archivo de requerimientos
COPY requirements.txt .

# Actualizamos e instalamos las dependencias básicas, MPI (MPICH) y otros paquetes necesarios
RUN apt-get update && \
    apt-get install -y psmisc bc mpich && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/bash"]
