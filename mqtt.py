import paho.mqtt.client as mqtt

class Mqtt():
    def __init__(self, host='localhost', port=1883, keepalive=60):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(host=host, port=port, keepalive=keepalive)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code: "+str(rc))
        self.subscribe("#/SYS", 0)
        self.subscribe("parking/machine/status", 0)
        self.subscribe("parking/machine/command", 2)

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def subscribe(self, channel=None, qos=0):
        if not channel:
            return
        
        self.client.subscribe(channel)
    
    def publish(self, topic, msg=None, qos=2, retain=False):
