# Parking Py

## Prerequisites
```shell
sudo apt-get install python3-pip python3-dev make gcc libevdev-dev i2c-tools libi2c-dev -y
```
Disable bluetooth, by adding below script to the bottom of `config.txt`
```shell
dtoverlay=disable-bt
```
## How to run the project
1. Install [pyenv](https://github.com/pyenv/pyenv)
2. Install python 3.8.13 using pyenv `pyenv install 3.8.13`
3. Create virtualenv using pyenv `pyenv virtualenv 3.8.13 parking`
4. Activate virtualenv `pyenv activate parking`
5. Confirm the python version using `python --version`
6. Install `requirements.txt` with pip `pip install -r requirements.txt`
7. Run main.py

## Some notes on the design
### Dashboard and communication
1. All communication use MQTT
2. Making sure on data format standarization is it using json, protobuf, or maybe a simple string and divided by semicolon `;`
### Gate Entry
1. Gate can be opened immediately without need to wait broker or web or dashboard send acknowledge response
2. After user scan the QR, save data to local db first (inmem, redis, or SQLite is okay) in case of lost connection
3. Send the data with QoS level 2, to make sure that data received by broker (or QoS level 1, but need validator on the dashboard)
### Gate Exit
1. When user scan the QR, send data using QoS level 1 directly to web so they can process the payment
2. Listen to the topic; when found mentioned machine_id and status, open the gate immediately

## Pinout

| RPi | Module | Notes |
| -- | ---- | --- |
| GPIO2 (I2C SDA) | LCD DATA | LCD 1602 |
| GPIO3 (I2C SCL) | LCD CLOCK | LCD 1602 |
| GPIO17 | TRIG | Ultrasonic |
| GPIO27 | ECHO | Ultrasonic |
| GPIO14 | TX | Gate Serial |
| GPIO15 | RX | Gate Serial |

> **Notes**: Ultrasonic and LCD use the same 5V, i think it give some noise to Ultrasonic, that's why it's not reliable... better to use separate power for it
