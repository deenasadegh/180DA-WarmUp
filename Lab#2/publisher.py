import paho.mqtt.client as mqtt
import time

# Define the Callback Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

# Initialize the MQTT Client
client = mqtt.Client()

# Assign the Callback Functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to the MQTT Broker
client.connect_async("mqtt.eclipseprojects.io")

# Start the Loop
client.loop_start()

try:
    # Publish messages to the same topic
    for i in range(10):
        client.publish("ece180d/test", "Message " + str(i), qos=1)
        time.sleep(1)  # Delay between messages
    print("Done Publishing")
except KeyboardInterrupt:
    print("Interrupted")

# Stop the loop and disconnect
client.loop_stop()
client.disconnect()
