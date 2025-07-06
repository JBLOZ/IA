FROM bitnami/spark:latest

# 1) Nos aseguramos de usar el usuario root (para poder crear ~/.ivy2)
USER root

# 2) Creamos el HOME y el dir de ivy
ENV HOME=/root
RUN mkdir -p /root/.ivy2/local

# 3) Copiamos todo el proyecto a /app
WORKDIR /app
COPY . /app

# 4) Arrancamos spark-shell en modo local[*] con UI en 4040
ENTRYPOINT ["spark-shell", \
            "--master", "local[*]", \
            "--conf", "spark.ui.port=4040" \
           ]