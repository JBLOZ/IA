FROM python:3.12.6-bullseye
WORKDIR /workdir
COPY requirements.txt .
RUN apt-get update && \
    apt-get install psmisc && \
    pip install --no-cache-dir -r requirements.txt 
ENTRYPOINT ["/bin/bash"]
