import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

solenoid = 27
solenoidOnOff = 22

GPIO.setup(solenoid, GPIO.OUT)
GPIO.setup(solenoidOnOff, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#sleep(120)#to allow Photometer parameters to be entered

solenoidFrequency = 0
while (int(solenoidFrequency) == 0):
    solenoidFrequency = raw_input('\nPlease input solenoid frequency in Hz?:\n')
    
solenoidFrequencyFactor = 1.0/int(solenoidFrequency)

while True:
    while (GPIO.input(solenoidOnOff) == True):
        #0.05s = one twentyth of a second = time solenoid energized.
        GPIO.output(solenoid, GPIO.HIGH)
        sleep(0.05)
        GPIO.output(solenoid), GPIO.LOW)
        sleep(solenoidFrequencyFactor)
