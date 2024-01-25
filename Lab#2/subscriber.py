import paho.mqtt.client as mqtt
import time

# Define the Callback Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ece180d/test", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

def on_message(client, userdata, message):
    print("Received message: '" + str(message.payload.decode("utf-8")) + "' on topic '" + message.topic + "'")
    # Here you can add your logic to increment the counter and add a delay

# Initialize the MQTT Client
client = mqtt.Client()

# Assign the Callback Functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to the MQTT Broker
client.connect_async("mqtt.eclipseprojects.io")

# Start the Loop
client.loop_start()

try:
    # Run the loop as long as needed
    while True:
        time.sleep(1)  # Keeps the loop running
except KeyboardInterrupt:
    # Graceful Exit on CTRL+C
    print("Disconnecting from broker")

# Stop the loop and disconnect
client.loop_stop()
client.disconnect()