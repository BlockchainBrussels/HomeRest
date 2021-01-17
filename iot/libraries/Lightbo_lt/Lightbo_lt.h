/*
  Lightbo_lt.h - Library for the https://lightbo.lt project.
  Copyright by Frederik Rousseau.
  GPL-3.0.
*/

#ifndef Lightbo_lt_h
#define Lightbo_lt_h

#include "Arduino.h"
#include "String.h"
#include "ESP8266WebServer.h"
#include "ESP8266HTTPClient.h"

class Lightbo_lt
{
  public:
    Lightbo_lt();
    void wifiConnect();
    void event(const char* message);
    void ping();
    int rfid(const char* rfid);
    int getStatus();
    int intrusion();

  private:
    const char* _serverUrlEvent;
    const char* _serverUrlPingTemp;
    String _serverUrlPing;
    HTTPClient _httpEvent;
    HTTPClient _httpPing;
};

#endif