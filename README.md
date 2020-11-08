# Welcome to LIGHTBO.LT!

## What is LIGHTBO.LT?

This Open Source project is created to handle a private home security project.

LIGHTBO.LT is a home security infrastructure made of:
1. A software backend running on a Raspberry/PC/server (anything that can run Python code)
1. Small electronic devices that will detect movements, based on IOT devices (Arduino, Wemos)
1. Arm/disarm console to arm or disarm the home security project, based on an IOT device with RFID reader (RFID can come from a badge or your smartphone for example)
1. Visible and hearable devices in case of intrusion, like a revolving light or a vibrating horn
1. Possible integration with your home automation system to on/off all the lights when an intrusion is detected (simple example)

## Specifications

The software backend has already many functionalities:
1. A website to access the Arm / Disarm functionalities of the home security system
1. An API to:
    1. Arm/disarm the system
    1. A ping for the IOT devices to detect physical deterioration
    1. A log functionality to know everything what happened

## What do I need?

Regarding IOT devices, Blockchain Brussels uses the WeMos D1 mini because it has integrated WiFi. There are multiple sensors that you can use to detect an intrusion, mainly infrared (HW-416 or HC-SR501) or wave detection (like the HB100 radar). There are many others that can be usefull but weren't tested (yet), for example laser beams.
The WeMos D1 mini devices are powered by USB. You can use the cabling in the house foreseen for the sensors/consoles/etc to power with 5V the WeMos devices. Some soldering experience can be handsome in some cases ;-)

The hardware is available at the webshop https://lightbo.lt, in case you have any question, just ask it!

## What do you find here?

Content of the LIGHTBO.LT project:
1. Find the server application in /server written in Python.
    1. The uWSGI integration for the application is in /uwsgi (used in Nginx).
1. Arduino code (IOT devices) is in /iot. Very cheap hardware!
    1. Tested with WeMos D1 mini (ESP8266 with WiFi)
    1. Sensors used:
        1. Infrared sensor HW-416/HC-SR501 (detect warm bodies)
        1. RFID sensor RC522 (RFID reader to enable/disable the system)
        1. Microwave sensor HB100 (detect anything moving, be carefull for the waves ;-)


## Requirements

pip3 install flask-ext flask-mysql flask-basicauth

virtualenv -p python3 venv 

## Sponsor(s) and creation

LIGHTBO.LT has been started by Frederik Rousseau (@LinoxBE), who donates his effort to the project. Blockchain Brussels owns the copyrights and sponsors the project. The project is Open Source, feel to use and change it at will.
Feel free to report bugs, log ideas, fire questions about anything related to the prject!
