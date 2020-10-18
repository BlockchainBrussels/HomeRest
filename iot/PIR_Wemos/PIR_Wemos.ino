#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <Ticker.h>
Ticker timer1;

#include <Lightbo_lt.h>

Lightbo_lt lightbolt;

int pirPin = 5; // PIR sensor is attached to D1 mini D1 pin which maps to pin 5 for arduino library
int motion;

void ICACHE_RAM_ATTR onTimerISR(){
    Serial.println("Timer");
    //lightbolt.ping();
}

void ICACHE_RAM_ATTR stateChange() //Interrupt function
{
    motion++; //motion = digitalRead(pirPin);
    Serial.println("INTERRUPT: Motion.");
}

void setup() {
  Serial.begin(115200);

  lightbolt.wifiConnect();

  pinMode(2,OUTPUT); // Init LED
  pinMode(pirPin, INPUT); // Set PIR pin as input pin

  attachInterrupt(digitalPinToInterrupt(pirPin), stateChange, RISING); // Sets the interrupt function, falling edge triggered interrupts.

  //Initialize Ticker every 5s
  timer1.attach(5, onTimerISR);
}

void loop() {
    if (motion > 0) //low = no motion, high = motion
    {
      digitalWrite(2,LOW); // LED ON
      Serial.println("LOOP: Motion.");
      lightbolt.event("Infrared motion detected");
      delay(1000);
      motion = 0;
      digitalWrite(2,HIGH); // LED OFF
    }
    else
    {
      delay(1000);
    }
    //lightbolt.ping();
}
