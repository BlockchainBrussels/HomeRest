//#include <Ticker.h>
//Ticker timer1;

#include <Lightbo_lt.h>

Lightbo_lt lightbolt;

int radarPin = 5; // PIR sensor is attached to D1 mini D1 pin which maps to pin 5 for arduino library
int motion;

/*void ICACHE_RAM_ATTR onTimerISR(){
    Serial.print("count:"); Serial.println(count);
}*/

void ICACHE_RAM_ATTR stateChange() //Interrupt function
{
  motion++;
  Serial.println("INTERRUPT: Motion.");
}

void setup()
{
  Serial.begin(115200);

  lightbolt.wifiConnect();

  pinMode(2,OUTPUT); // Init LED
  pinMode(radarPin, INPUT); // Set PIR pin as input pin

  attachInterrupt(digitalPinToInterrupt(radarPin), stateChange, RISING); // Sets the interrupt function, falling edge triggered interrupts.
   
  //Initialize Ticker every 0.5s
  //timer1.attach(0.5, onTimerISR);
}

void loop()
{
    if (motion > 0) //low = no motion, high = motion
    {
      digitalWrite(2,LOW); // LED ON
      Serial.println("LOOP: Motion.");
      lightbolt.event("Radar motion detected");
      delay(1000);
      motion = 0;
      digitalWrite(2,HIGH); // LED OFF
    }
    else
    {
      delay(1000);
    }
    lightbolt.ping();
}
