# CSF
Python Code for CSF flow model experiments.
Thanks to flohwie for the MCP3201 rpi code
https://github.com/flohwie/raspi-MCP3201

Instructions for use: -

requires pigpio library see : http://abyz.me.uk/rpi/pigpio/download.html


1 in the terminal enter

  sudo pigpiod
  
2 to run the program enter
  
  python MCP3201Photometer.py
  
  you will be prompted for a file name and sampling frequency in Hertz
  
3  Data will be recorded while 3.3v is suppied to pin 17 (Broadcom Numbering)

4 Ctrl + C to exit
  
Instructions for CSFCamera.py

Type the command (without the double quotes and with the stars replaced by your choice of numbers.
The 'uniqueRunName' should be your choice of a unique name for the run and must be in 'quotes' and contain no spaces or special characters.): -
"nohup python3 CSFCamera.py --Frequency ** --DutyCycle ** --TimeLapse **** --RunFolder 'uniqueRunName'"
To terminate press and hold Ctrl & C or Cmd & C.
TimeLapse is the number of seconds between image captures e.g.
half an hour would be 1800.

