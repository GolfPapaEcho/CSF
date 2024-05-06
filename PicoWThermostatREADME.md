This is a simple thermostat controlled by the RPi Pico W written in micropython.

It uses the DS18x20 temperature sensor on GP26 and a power transistor on GP22  
goes to the heater (we used nichrome wire c. 8ohm/m).

It severs up a webpage where you can adjust the setpoint and see the setpoint
and sensor temperatures (the sensor temperature is updated every 5 seconds on
the webpage).

Just edit the secrets.py with your SSID and PASSWORD and upload the main.py and
adjusted secrets.py code to the Pico W in the same folder and away you go!

:-) GPE  
