# Importing modules
import spidev               # To communicate with SPI devices
#from numpy import interp    # To scale values
from time import sleep      # To add delay
import RPi.GPIO as GPIO     # To use GPIO pins
import csv

GPIO.setmode(GPIO.BCM)

actionSwitch = 17


GPIO.setup(actionSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0)


# Read MCP3204 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&15) << 8) + adc[2]
  return data


#menu
fileName1 = raw_input('Please enter file name?:\n')
pollFrequency = raw_input('\nPlease input sensor polling frequency in Hz?:\n')
pollFrequencyFactor = 1.0/int(pollFrequency)



#the infinite loop where the values are read and written to csv
#while True:
#n = 0#for while loop
with open(('/home/pi/Documents/CSF/'+fileName1+'.csv'), 'a+') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")

    writer.writerow(['Time/s', 'Value'])

    while True:
        n=0
        while (GPIO.input(actionSwitch) == True):
            
            output = analogInput(0) # Reading from CH0
            writer.writerow([n, output])
            n = n + pollFrequencyFactor
            sleep(pollFrequencyFactor)


    #output = interp(output, [0, 1023], [0, 100])
    #print(output)
    #sleep(0.05) #values are displayed every 50ms
