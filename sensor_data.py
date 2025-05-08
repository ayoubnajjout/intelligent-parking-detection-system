import random
import time
import paho.mqtt.client as mqtt

# MQTT broker configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/car_detection"

# MQTT Client Setup
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

def simulate_sensor_data():
    while True:
        # Simulate a random distance between 5 cm and 100 cm
        distance_cm = round(random.uniform(5, 100), 2)
        print(f"Publishing distance: {distance_cm} cm")
        
        # Publish the numeric distance value
        mqtt_client.publish(MQTT_TOPIC, str(distance_cm))
        
        time.sleep(2)

if __name__ == "__main__":
    simulate_sensor_data()
