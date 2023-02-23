#include <HardwareSerial.h>
#include "WiFi.h"
#include "AsyncTCP.h"
#include <ESPAsyncWebServer.h>
#include <Wire.h>

HardwareSerial SerialPort(2); // use UART2

// Set your access point network credentials
const char* ssid = "ESP32-Access-Point";
const char* password = "123456789";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);


char number[]  = " ";
char data_send[] = " ";
String readData() {
  char* a = number;
  String b = String(a);
  return b;
  //return String(1.8 * bme.readTemperature() + 32);
}

void setup()
{
//  Serial.begin(9600);
  SerialPort.begin(9600, SERIAL_8N1, 16, 17);

    // Serial port for debugging purposes
  Serial.begin(115200);
  Serial.println();
  
  // Setting the ESP as an access point
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);


  server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request){
    //request->send_P(200, "text/plain", readData().c_str());
    //request->send_P(200, "text/plain", String(number[0]).c_str());
    request->send_P(200, "text/plain", String(data_send[0]).c_str());
  });
  
  server.begin();
  
}
void loop()
{
  delay(10);
  if (SerialPort.available() > 0 )
  {
      number[0] = SerialPort.read();
      Serial.println(number[0]);
      if( number[0] == '1' || number[0] == '2' || number[0] == '3'){
        data_send[0] = number[0];
      }

  }
}
