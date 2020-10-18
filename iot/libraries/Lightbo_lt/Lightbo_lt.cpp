/*
  Lightbo_lt.cpp - Library for the https://lightbo.lt project.
  Copyright by Frederik Rousseau.
  GPL-3.0.
*/

#include "ESP8266WiFi.h"
#include "WiFiClient.h"
#include "Lightbo_lt.h"
#include "Lightbo_lt_security.h"

Lightbo_lt::Lightbo_lt()
{
  _serverUrlEvent = linkEvent;
  _serverUrlPingTemp = linkPing;
}

void Lightbo_lt::wifiConnect()
{
  Serial.print("connecting to "); Serial.print(wifiSsid); Serial.print(" ");
  WiFi.mode(WIFI_STA);
  WiFi.begin(wifiSsid, wifiPassword);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" WiFi connected!");
  Serial.print("IP address: "); Serial.println(WiFi.localIP());
  delay(2000);

  // Add the IP address in the URL
  //Serial.print("_serverUrlPingTemp BEFORE modification : "); Serial.println(_serverUrlPingTemp);
  _serverUrlPing = String(_serverUrlPingTemp) + "/" + WiFi.localIP().toString().c_str();
  //Serial.print("_serverUrlPing AFTER modification : "); Serial.println(_serverUrlPing.c_str());
}

void Lightbo_lt::event(const char* message)
{
    _httpEvent.begin(_serverUrlEvent); //Specify request destination
    _httpEvent.addHeader("Content-Type", "application/json");
    char textToPost[100] = "{\"device\":\""; strcat(textToPost,WiFi.localIP().toString().c_str()); strcat(textToPost,"\",\"event\":\""); strcat(textToPost,message); strcat(textToPost,"\"}");
    Serial.print(_serverUrlEvent); Serial.print(" - "); Serial.println(textToPost);
    _httpEvent.POST(textToPost);
    _httpEvent.writeToStream(&Serial);
    //Serial.println(_httpEvent.getString()); //Print request response payload
    _httpEvent.end();
}

void Lightbo_lt::ping()
{
    //Serial.print("Ping "); Serial.print(_serverUrlPing.c_str()); Serial.print(" : "); 
    _httpPing.begin(_serverUrlPing.c_str()); //Specify request destination
    _httpPing.POST("Hello!");
    _httpPing.writeToStream(&Serial);
    //Serial.println(_httpPing.getString()); //Print request response payload
    _httpPing.end();
}

int Lightbo_lt::rfid(const char* rfid)
{
    char textForFullActionUrl[100] = ""; strcat(textForFullActionUrl,linkAction); strcat(textForFullActionUrl,"/switch/"); strcat(textForFullActionUrl,WiFi.localIP().toString().c_str()); strcat(textForFullActionUrl,"/"); strcat(textForFullActionUrl,rfid);
    HTTPClient httpRfid;
    httpRfid.begin(textForFullActionUrl); //Specify request destination
    int httpCode = httpRfid.POST("Switch!");
    httpRfid.writeToStream(&Serial);
    //String response = httpRfid.getString(); // TODO: getString takes 5 seconds !!!!!!!
    httpRfid.end();
    return httpCode;
    //Serial.println("END");
    //WiFiClient client;
    //client.print(String("GET ") + String("/action/switch/") + WiFi.localIP().toString() + " HTTP/1.1\r\n" + "Host: 192.168.1.7" + "\r\n" + "Connection: close\r\n\r\n");
}

int Lightbo_lt::getStatus()
{
    HTTPClient httpStatus;
    httpStatus.begin(linkStatus); //Specify request destination
    int httpCode = httpStatus.GET();
    //Serial.print(" httpCode: "); Serial.println(httpCode);
    //httpStatus.writeToStream(&Serial);
    httpStatus.end();
    return httpCode;
}
