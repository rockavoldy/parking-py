FROM python:3.8.13-slim-buster

WORKDIR /app
RUN apt-get update
RUN apt-get install make gcc -y
RUN apt-get install libevdev-dev i2c-tools libi2c-dev -y

COPY requirements.txt requirements.txt
RUN pip install smbus pigpio
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
