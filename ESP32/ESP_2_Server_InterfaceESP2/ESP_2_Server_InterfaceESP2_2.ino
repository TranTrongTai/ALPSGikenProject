
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>

const char* ssid = "ESP32-Access-Point";
const char* password = "123456789";

//Your IP address or domain name with URL path
const char* serverData = "http://192.168.4.1/data";



unsigned long previousMillis = 0;
const long interval = 2000; 
String get_data;


#define RELAY_PIN_1 14 // ESP32 pin GIOP16 connected to the IN pin of relay
#define RELAY_PIN_2 27

void setup() {
  Serial.begin(115200);
  
  pinMode(RELAY_PIN_1, OUTPUT);
  pinMode(RELAY_PIN_2, OUTPUT);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  unsigned long currentMillis = millis();
  
  if(currentMillis - previousMillis >= interval) {
     // Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED ){ 
      get_data = httpGETRequest(serverData);
      Serial.println(get_data);
       digitalWrite(RELAY_PIN_1, HIGH);
       digitalWrite(RELAY_PIN_2, HIGH);
      if(get_data == "1"){
        digitalWrite(RELAY_PIN_1, LOW);  
      }
      if(get_data == "2"){
        digitalWrite(RELAY_PIN_1, LOW);  
        digitalWrite(RELAY_PIN_2, LOW); 
      }
      else if(get_data == "3"){
        delay(50);
        digitalWrite(RELAY_PIN_1, HIGH);
        digitalWrite(RELAY_PIN_2, HIGH);
      }
      // save the last HTTP GET Request
      previousMillis = currentMillis;
    }
    else {
      Serial.println("WiFi Disconnected");
    }
  }
}

String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;
    
  // Your Domain name with URL path or IP address with path
  http.begin(client, serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "--"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}
