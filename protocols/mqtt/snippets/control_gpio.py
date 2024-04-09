import random
import argparse
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client
import re
import json

# Control a GPIO pin via MQTT

GPIO_PIN = 17

def assert_valid_topic(topic):
    assert re.match(r'^[a-zA-Z0-9]+/rx$', topic), "Topic format should be 'ID/rx' where ID is alphanumeric"

def setup_gpio(led_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin, GPIO.OUT)

def connect_mqtt(broker, port, client_id, username, password):
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
    client.tls_set(tls_version=mqtt_client.ssl.PROTOCOL_TLS)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client, topic, led_pin):
    def on_message(client, userdata, msg):
        msg_payload = msg.payload.decode()
        print(f"Received `{msg_payload}` from `{msg.topic}` topic")
        if msg_payload == "on":
            GPIO.output(led_pin, GPIO.HIGH)  # Turn LED on
        elif msg_payload == "off":
            GPIO.output(led_pin, GPIO.LOW)  # Turn LED off

        # Device control implies request/response semantics
        # So we acknowledge the message by sending a response
        pub_topic = f"{msg.topic[:-3]}/tx"
        client.publish(pub_topic, "ΟΚ")
        
    client.subscribe(topic)
    client.on_message = on_message

def run(broker, port, client_id, username, password, topic):
    setup_gpio(led_pin=GPIO_PIN)
    client = connect_mqtt(broker, port, client_id, username, password)
    subscribe(client, topic, GPIO_PIN)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()
        client.disconnect()


def parse_args():
    parser = argparse.ArgumentParser(description='MQTT Client Arguments')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--broker', type=str, help='MQTT broker address')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port (default: 1883)')
    parser.add_argument('--username', type=str, help='MQTT username')
    parser.add_argument('--password', type=str, help='MQTT password')
    parser.add_argument('--topic', type=str, help='MQTT topic to subscribe to (of the form: ID/rx)')
    args = parser.parse_args()

    if args.config:
        config = load_config(args.config)
        args.broker = config.get('broker', args.broker)
        args.port = config.get('port', args.port)
        args.username = config.get('username', args.username)
        args.password = config.get('password', args.password)
        args.topic = config.get('topic', args.topic)

    return args

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    args = parse_args()

    assert_valid_topic(args.topic)
    client_id = f'python-mqtt-{random.randint(0, 1000)}'

    # Debug
    print("Broker:", args.broker)
    print("Port:", args.port)
    print("Username:", args.username)
    print("Password:", args.password)
    print("Topic:", args.topic)
    print("Client ID:", client_id)

    run(args.broker, args.port, client_id, args.username, args.password, args.topic)
