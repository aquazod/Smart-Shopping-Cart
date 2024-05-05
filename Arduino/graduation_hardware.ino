#include <WiFi.h>
#include "HX711.h"

#define DOUT  19
#define CLK  18
// right wight green left red black 
HX711 scale;

const char* ssid = "att";
const char* password = "ASsygdasddAUDGHI6567";// Replace with the Password of your WIFI
const char* host = "192.168.43.155"; // Replace with the IP address of your Python script

void setup() {
  Serial.begin(115200);
  delay(1000);
  scale.begin(DOUT, CLK);

  scale.set_scale(2280.f); // Set the scale factor to your load cell's specification
  scale.tare(); // Reset the scale to 0
  delay(500);
  scale.tare();

  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
}

void loop() {
  float weight = scale.get_units(); // get the weight in kg
  Serial.println("Weight: " + String(weight) + " kg");
  WiFiClient client;
  if (client.connect(host, 80)) { // connect to the Python script server
    client.print("GET /?weight=" + String(weight) + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n\r\n");
    delay(10);
    client.stop();
  }
  
  delay(1000);
}