import argparse
import random
from paho.mqtt import client as mqtt_client

# Note: This snippet is a subscriber that listens to a specific topic on the MQTT broker.
# It uses V2 of the Paho MQTT client API

def connect_mqtt(broker, port, client_id, username, password):
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def run(broker, port, client_id, username, password, topic):
    client = connect_mqtt(broker, port, client_id, username, password)
    subscribe(client, topic)
    client.loop_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MQTT Client Arguments')
    parser.add_argument('--broker', type=str, required=True, help='MQTT broker address')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port (default: 1883)')
    parser.add_argument('--username', type=str, required=True, help='MQTT username')
    parser.add_argument('--password', type=str, required=True, help='MQTT password')
    parser.add_argument('--topic', type=str, required=True, help='MQTT topic to subscribe to')
    args = parser.parse_args()

    client_id = f'python-mqtt-{random.randint(0, 1000)}'

    run(args.broker, args.port, client_id, args.username, args.password, args.topic)
