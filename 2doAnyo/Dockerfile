FROM python:3.9.20-bullseye
WORKDIR /workdir
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["/bin/bash"]
