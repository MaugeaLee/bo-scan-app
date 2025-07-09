import logging
import threading

import paho.mqtt.client as mqtt

from API.CONFIG.bogger import BoggerDevLogger
from API.CONFIG.static import *


class BoMQTTClient:
    def __init__(self, broker="localhost", port=1883, logger:logging.Logger=None):
        self.logger = logger or BoggerDevLogger(self.__class__.__name__).logger
        self.broker = broker
        self.port = port

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(response_scan_topic)
        self.logger.info("Subscribed to " + response_scan_topic + f"rc: {rc}")

    def on_disconnect(self, client, userdata, rc):
        self.client.unsubscribe(response_scan_topic)
        self.logger.info("Unsubscribed from " + response_scan_topic + f" rc: {rc}")

    def on_message(self, client, userdata, msg):
        self.logger.info(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.logger.info(f"Connected to broker: {self.broker}:{self.port}")

    def disconnect(self):
        self.client.disconnect()
        self.logger.info(f"Disconnected from broker: {self.broker}:{self.port}")

    def loop_start(self):
        self.client.loop_start()
        self.logger.info("MQTT Loop forever Start")

    def publish(self, topic: str, message: str):
        self.client.publish(topic, message, qos=1, retain=True)
        self.logger.info(f"Published to topic: {topic}  / message: {message}")


if __name__ == "__main__":
    mqtt_client = BoMQTTClient()
    mqtt_client.connect()
    mqtt_client.loop_forever()


