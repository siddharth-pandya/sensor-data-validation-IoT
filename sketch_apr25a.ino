const int refresh=1;//3 seconds
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// DHT settings starts
#include "DHT.h"
#define DHTPIN 2     // what digital pin we're connected to
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);
float tValue;
// ****** DHT settings end

#include <WiFiClient.h>
#include <ESP8266mDNS.h>
#ifndef STASSID
#define STASSID "iPhone_19" // Your WiFi SSID
#define STAPSK  "qwerty123" //Your WiFi password
#endif

const char* ssid = STASSID;
const char* password = STAPSK;
ESP8266WebServer server(80);

void sendTemp() {
  String page = "<!DOCTYPE html>";
  page +="    <meta http-equiv='refresh' content='";
  page += String(refresh);// how often temperature is read
  page +="'/>"; 
  page +="<html>";
  page +="<body>";
  page +="<p style=\"font-size:50px;\">Temperature<br/>"; 
  page +="<p style=\"color:red; font-size:50px;\">";
  page += String(tValue, 2);
  page +="</p>"; 
  page +="</body>"; 
  page +="</html>"; 
  server.send(200,  "text/html",page);
}

void handleNotFound() {

  String message = "File Not Found";
  message += "URI: ";
  message += server.uri();
  message += "Method: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "Arguments: ";
  message += server.args();
  message += "";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "";
  }
  server.send(404, "text/plain", message);
}

void setup(void) {

  dht.begin();
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  if (MDNS.begin("robojaxDHT")) {
    Serial.println("MDNS responder started");
  }
  server.on("/", sendTemp);
  server.on("/inline", []() {
    server.send(200, "text/plain", "this works as well");
  });
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
  float c = dht.readTemperature();// Read temperature as Celsius (the default)
  Serial.println(c);
  tValue =c;
  delay(300);// change this to larger value (1000 or more) if you don't need very often reading
}
