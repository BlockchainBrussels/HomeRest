# Welcome to lightbo.lt!

This Open Source project is created to handle a private home security project. The idea is to use cheap IOT devices with sensors as intrusion detection.

The project has a website to access the Arm / Disarm functionalities of the alarm system. And an API to do the arm/disarm, the pings, and to log everything happening.

I use the WeMos D1 mini because it has integrated WiFi. There are multiple sensors that you can use to detect an intrusion, mainly infrared (HW-416 or HC-SR501) and wave detector (like the HB100). There are many others that are usefull, for example laser beams.
My devices are powered by USB, using the cabling in the house foreseen for the sensors/keyboards/etc of an alarm system.

1. Find the server application in /server written in Python.
1. The uWSGI integration in /uwsgi (used in Nginx).
1. Client code (IOT devices) is in /client. Hardware cheaply available on AliExpress!
    1. Tested with WeMos D1 mini (ESP8266 with WiFi) +-$2.
    1. Sensors used:
        1. Infrared sensor HW-416/HC-SR501 (detect warm bodies, cost +-$2)
        1. RFID sensor RC522 (RFID reader to enable/disable the system, cost +-$2)
        1. Microwave sensor HB100 (detect anything moving!, cost +-$8, , be carefull for the waves ;-)
