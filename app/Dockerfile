FROM ubuntu:22.04
WORKDIR /usr/src/app
COPY requirements.txt .
RUN apt-get update
RUN apt-get install -y \
    python3-pip \
    libpq-dev \
    python3-dev
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python3","driver.py"]
