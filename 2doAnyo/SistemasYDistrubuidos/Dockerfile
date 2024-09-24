FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y sudo gcc g++ && \
    sudo apt update && \
    sudo apt install psmisc
WORKDIR /home/usuario
COPY . .
RUN useradd -ms /bin/bash usuario
USER root
RUN chmod +x /home/usuario/start.sh
CMD ["/home/usuario/start.sh"]
