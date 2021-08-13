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
    
period = float(1.0/int(solenoidFrequency))

dutyCyclePercent = 0
while (int(dutyCyclePercent) == 0):
    dutyCyclePercent = raw_input('\nPlease enter duty cycle percentage in range 1 to 100:\n')
dutyCyclePercent = float(dutyCyclePercent)
dutyCycle = float(dutyCyclePercent*period/100)

while True:
    while (GPIO.input(solenoidOnOff) == True):
        #0.05s = one twentyth of a second = time solenoid energized.
        GPIO.output(solenoid, GPIO.HIGH)
        sleep(dutyCycle)
        GPIO.output(solenoid, GPIO.LOW)
        sleep((period-dutyCycle))
