import paho.mqtt.client as mqtt


if __name__ == "__main__":
    broker_ip = "localhost"
    broker_port = 1883
    topic = "test/topic"


    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(topic)

    def on_disconnect(client, userdata, rc):
        print("Disconnected with result code " + str(rc))
        client.unsubscribe(topic)

    def on_message(client, userdata, msg):
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect(broker_ip, broker_port, 60)
    client.loop_forever()