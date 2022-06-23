# Parking Py

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
| GPIO3 (I2C SCL) | LCD CLOCK | LCD1602 |
| GPIO17 | TRIG | Ultrasonic |
| GPIO27 | ECHO | Ultrasonic |

> **Notes**: Ultrasonic and LCD use the same 5V