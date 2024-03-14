#include <WiFi.h>
#include <PubSubClient.h>
#include "arduino_secrets.h"
#include "ICM_20948.h"

#define SERIAL_PORT Serial

#ifdef USE_SPI
#define SPI_PORT SPI
#define CS_PIN 2
ICM_20948_SPI myICM;
#else
#define WIRE_PORT Wire
#define AD0_VAL 1
ICM_20948_I2C myICM;
#endif

const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

const char *mqtt_broker = "mqtt.eclipseprojects.io";
const char *topic = "myUniqueIMUTopic/data";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  SERIAL_PORT.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    SERIAL_PORT.println("Connecting to WiFi..");
  }
  SERIAL_PORT.println("Connected to the WiFi network");

  client.setServer(mqtt_broker, mqtt_port);
  while (!client.connected()) {
    String client_id = "esp32-client-";
    client_id += String(WiFi.macAddress());
    if (client.connect(client_id.c_str())) {
      SERIAL_PORT.println("Connected to MQTT Broker!");
    } else {
      SERIAL_PORT.print("Failed with state ");
      SERIAL_PORT.print(client.state());
      delay(2000);
    }
  }

  #ifdef USE_SPI
  SPI_PORT.begin();
  myICM.begin(CS_PIN, SPI_PORT);
  #else
  WIRE_PORT.begin();
  WIRE_PORT.setClock(400000);
  myICM.begin(WIRE_PORT, AD0_VAL);
  #endif

  bool initialized = false;
  while (!initialized) {
    if (myICM.status != ICM_20948_Stat_Ok) {
      SERIAL_PORT.print("Initialization of the sensor failed with status: ");
      SERIAL_PORT.println(myICM.statusString());
      delay(500);
    } else {
      initialized = true;
      SERIAL_PORT.println("Sensor initialized successfully");
    }
  }
}

void loop() {
  if (myICM.dataReady()) {
    myICM.getAGMT();

    char buf[256];
    snprintf(buf, sizeof(buf), "%f %f %f %f %f %f",
             myICM.gyrX(), myICM.gyrY(), myICM.gyrZ(),
             myICM.accX(), myICM.accY(), myICM.accZ());
    client.publish(topic, buf);
    SERIAL_PORT.println(buf);

    client.loop();
    delay(100);
  }
}
