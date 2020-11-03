#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

#include <Lightbo_lt.h>

Lightbo_lt lightbolt;

#define SS_PIN D8 //Pin on WeMos D1 Mini
#define RST_PIN D3 //Pin on WeMos D1 Mini
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;

void setup()
{
  Serial.begin(115200);
  
  lightbolt.wifiConnect();

  pinMode(D1, OUTPUT);
  SPI.begin();
  rfid.PCD_Init();

  pinMode(2,OUTPUT); // Init LED
}

void loop(void) {
  delay(700);
  handleRFID();

  // Status (http response code): 201==armed, 200=disarmed
  int status = lightbolt.getStatus(linkStatus);
  //Serial.print("Status: "); Serial.println(status);
  if( status == 201 )
      digitalWrite(2,LOW); // LED ON
  else
      digitalWrite(2,HIGH); // LED OFF
}

void handleRFID() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  String card_uid = printHex(rfid.uid.uidByte, rfid.uid.size);
  
  //String ausgabe = "/rfid/" + String(card_uid);
  Serial.println("");
  Serial.print("sending card_uid to server: ");
  Serial.print(card_uid);
  Serial.print(" - ");
  
  int status = lightbolt.rfid(card_uid.c_str());
  if( status == 201 ){
      digitalWrite(2,LOW); // LED ON
      delay(100);digitalWrite(2,HIGH); // LED OFF
      delay(100);digitalWrite(2,LOW); // LED ON
      delay(100);digitalWrite(2,HIGH); // LED OFF
      delay(100);digitalWrite(2,LOW); // LED ON
 }
  else{
      digitalWrite(2,HIGH); // LED OFF
      delay(100);digitalWrite(2,LOW); // LED ON
      delay(100);digitalWrite(2,HIGH); // LED OFF
      delay(100);digitalWrite(2,LOW); // LED ON
      delay(100);digitalWrite(2,HIGH); // LED OFF
  }
  Serial.println("[OK]");
  delay(1200);
}

String printHex(byte *buffer, byte bufferSize) {
  String id = "";
  for (byte i = 0; i < bufferSize; i++) {
    id += buffer[i] < 0x10 ? "0" : "";
    id += String(buffer[i], HEX);
  }
  return id;
}
