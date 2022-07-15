import paho.mqtt.client as mqtt
import time

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
        self.subscribe("local/machine/status", 0)
        self.subscribe("local/machine/command", 2)

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    # publish local command; should be used to send local command 
    # (open gate; start scanning QR; start checking if vehicle already passing the gate or not, and such)
    def format_local_command(self, machine_id, command, target):
        """ Format local command to "machine_id;command;target;timestamp"
            params: machine_id str: The unique ID to know which machine this command from
            params: command str: what command published
            params: target str: target for the command to be run; for what process

            return: formatted string delimited by ; (semi-colon)
        """
        timestamp = self._get_ms_timestamp()
        return "{};{};{};{}".format(machine_id, command, target, timestamp)

    def publish_local_command(self, machine_id, command, target):
        msg = self.format_local_command(machine_id, command, target)
        self.publish("local/machine/command", msg=msg, qos=2)
    
    # publish command; should be used to send data from the machine to dashboard
    def format_command(self, machine_id, command, data):
        """ Format local command to "machine_id;command;timestamp"
            params: machine_id str: The unique ID to know which machine this command from
            params: command str: what command published
            params: data str: data from scanned QR; to be saved to the db later

            return: formatted string delimited by ; (semi-colon)
        """
        # NOTE: there is no target here, because command formatted by this method 
        # should be consumed by dashboard

        timestamp = self._get_ms_timestamp()
        return "{};{};{};{}".format(machine_id, command, data, timestamp)

    def publish_command(self, machine_id, command, data):
        msg = self.format_command(machine_id, command, data)
        self.publish("parking/machine/command", msg=msg, qos=2)
    
    # status message; can be used locally, and remotely
    def format_status_message(self, machine_id, status):
        """ Format status message, maybe needed, or maybe not, but it's not hurt to publish status """
        timestamp = self._get_ms_timestamp()
        return "{};{};{}".format(machine_id, status, timestamp)

    def publish_status(self, topic, machine_id, status):
        msg = self.format_status_message(machine_id, status)
        self.publish(topic, msg=msg, qos=0)

    # internal
    def subscribe(self, channel=None, qos=0):
        if not channel:
            return
        
        self.client.subscribe(channel)
    
    def publish(self, topic, msg=None, qos=0, retain=False):
        self.client.publish(topic, payload=msg, qos=qos, retain=retain)

    def _get_ms_timestamp(self):
        # return timestamp in milliseconds
        return int(time.time_ns() / 1000000)