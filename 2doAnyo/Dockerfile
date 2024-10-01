FROM python:3.10-bullseye
WORKDIR /workdir
COPY requirements.txt .
RUN apt-get update && \
    apt-get install psmisc && \
    pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["/bin/bash"]
