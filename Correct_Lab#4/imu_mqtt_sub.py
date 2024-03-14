import paho.mqtt.client as mqtt
import time
import re
import numpy as np
from collections import deque

MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = "myUniqueIMUTopic/data"

# Moving average settings
window_size = 10
gyro_x_history = deque(maxlen=window_size)
gyro_y_history = deque(maxlen=window_size)
gyro_z_history = deque(maxlen=window_size)

def moving_average(new_value, history):
    history.append(new_value)
    return np.mean(history)

def classify_action(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z):
    # Update moving averages
    gyro_x_avg = moving_average(gyro_x, gyro_x_history)
    gyro_y_avg = moving_average(gyro_y, gyro_y_history)
    gyro_z_avg = moving_average(gyro_z, gyro_z_history)

    # Calculate magnitudes using moving averages
    gyro_magnitude_avg = np.sqrt(gyro_x_avg**2 + gyro_y_avg**2 + gyro_z_avg**2)

    # Define thresholds
    gyro_idle_threshold = 2.0
    gyro_motion_threshold = 6.0
    gyro_rotation_threshold = 10.0
    non_rotation_threshold = 1.0  # Threshold for y and z axes to avoid misclassifying as rotation

    # Classification logic
    if gyro_magnitude_avg < gyro_idle_threshold:
        return "Idle"
    elif abs(gyro_z_avg) > gyro_rotation_threshold:
        return "Circular Rotation"
    elif abs(gyro_x) > gyro_motion_threshold:
        return "Upward Lift"  # Movement in the +x direction with minimal rotation
    elif abs(gyro_z) > gyro_motion_threshold:
        return "Forward Push"

    return "Idle"  # Default to idle if conditions for other actions are not met

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC, qos=1)

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", payload)
    if len(numbers) == 6:  # 3 gyroscope and 3 accelerometer values
        gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = map(float, numbers)
        action = classify_action(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z)
        print(f"Classified Action: {action}")
    else:
        print("Unexpected data format")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting from broker")
    client.loop_stop()
    client.disconnect()
