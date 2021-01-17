#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

#include <Lightbo_lt.h>

Lightbo_lt lightbolt;


void setup()
{
  Serial.begin(115200);
  
  lightbolt.wifiConnect();

  pinMode(D1, OUTPUT);
  pinMode(2,OUTPUT); // Init LED
  digitalWrite(2,HIGH); // LED OFF
}

void loop(void) {
  // Status (http response code): 201==armed, 200=disarmed
  /*int status = lightbolt.getStatus();
  Serial.print("Status: "); Serial.println(status);
  if( status == 201 )
      digitalWrite(2,LOW); // LED ON
  else
      digitalWrite(2,HIGH); // LED OFF
  */

  // intrusionDetected == False, then httpCode == 200
  // intrusionDetected == True,  then httpCode == 201
  if (lightbolt.intrusion() == 201){
      digitalWrite(2,LOW); // LED ON
      digitalWrite(D1, LOW); // activate relay
  }else{
      digitalWrite(2,HIGH); // LED OFF
      digitalWrite(D1, LOW); // activate relay
  }

  delay (1000);
}
