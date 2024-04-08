import random
import argparse
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client

# Control a GPIO pin via MQTT

GPIO_PIN = 17

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
