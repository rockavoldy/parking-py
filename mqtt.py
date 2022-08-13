import paho.mqtt.client as mqtt
import time
from helper import Helper

class Mqtt():
    def __init__(self, host='localhost', port=1883, keepalive=60, username=None, password=None):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        if username and password:
            # When username and password set, connect to mqtt with username and password
            self.client.username_pw_set(username, password)

        self.client.connect(host=host, port=port, keepalive=keepalive)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code: "+str(rc))
        self.subscribe("parking/machine/status", 0)
        self.subscribe("parking/machine/command", 0)

    def on_message(self, client, userdata, msg):
        # since there is no message from web, only publish-publish-publish, this method
        # won't be used, just print here for debug
        print(msg.topic+" "+str(msg.payload))
    
    # publish command; should be used to send data from the machine to dashboard
    def format_command(self, machine_id, command, data):
        """ Format local command to "machine_id;command;timestamp"
            params: machine_id str: The unique ID to know which machine this command from
            params: command str: what command published; checkin OR checkout
            params: data str: data from scanned QR; to be saved to the db later

            return: formatted string delimited by ; (semi-colon)
        """
        # NOTE: there is no target here, because command formatted by this method 
        # should be consumed by dashboard
        # NOTE: expired time; only used on checkout, if time_now > expired
        # don't open the gate and print (check your phone again)

        timestamp = self._get_ms_timestamp()
        return {
            'machine_id': machine_id,
            'command': command, # checkin, checkout
            'data': data, # data from QRIS
            'timestamp': timestamp,
        }

    def publish_command(self, machine_id, command, data):
        msg = self.format_command(machine_id, command, data)
        msg = Helper.format_json_mqtt(msg)

        res = self.publish("parking/machine/command", msg=msg, qos=1)
        print(res)
        print(res.rc)
        print("is success", res.rc == mqtt.MQTT_ERR_SUCCESS)
        print('is no connec', res.rc == mqtt.MQTT_ERR_NO_CONN)
        print('mqtt err no queue', res.rc == mqtt.MQTT_ERR_QUEUE_SIZE)
        print(res.is_published)
        print(res.mid)
    
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
        self.client.reconnect()
        return self.client.publish(topic, payload=msg, qos=qos, retain=retain)

    def _get_ms_timestamp(self):
        # return timestamp in milliseconds
        return int(time.time_ns() / 1000000)
