import logging
import threading

import paho.mqtt.client as mqtt

from API.CONFIG.bogger import BoggerDevLogger


class MQTTClient:
    def __init__(self, broker="localhost", port=1883, topic="#", logger:logging.Logger=None):
        self.logger = logger or BoggerDevLogger(self.__class__.__name__).logger
        self.broker = broker
        self.port = port
        self.topic = topic
        self.connected = False
        self.thread= None

        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        self.connected = True
        self.client.subscribe(self.topic)
        self.logger.info("Connected to broker")

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        self.client.unsubscribe(self.topic)
        self.logger.info("Disconnected from broker")

    def on_message(self, client, userdata, msg):
        self.logger.info(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")

    def start(self):
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)
        self.thread = threading.Thread(target=self.client.loop_forever)
        self.thread.daemon = True
        self.thread.start()
        self.logger.info("MQTT Client started.")

    def stop(self):
        self.client.disconnect()
        self.logger.info("MQTT Client stopped.")




if __name__ == "__main__":
    mqtt_client = MQTTClient(topic="test/topic")
    mqtt_client.start()
