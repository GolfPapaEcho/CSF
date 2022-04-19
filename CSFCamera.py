import datetime;
from time import sleep
from picamera import PiCamera
import RPi.GPIO as GPIO
import argparse as argp

GPIO.setmode(GPIO.BCM)


solenoid = 27
solenoidOnOff = 22

GPIO.setup(solenoid, GPIO.OUT)
GPIO.setup(solenoidOnOff, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

parser = argp.ArgumentParser(description='Input frequency in Hertz then duty cycle as percentage.')
parser.add_argument('--Frequency', type=float, required=True)
parser.add_argument('--DutyCycle', type=float, required=True)
args = parser.parse_args()
solenoidFrequency = args.Frequency

period = float(1.0/float(solenoidFrequency))
dutyCyclePercent = args.DutyCycle

dutyCyclePercent = float(dutyCyclePercent)
dutyCycle = float(dutyCyclePercent*period/100)


camera = PiCamera()
#camera.start_preview()
sleep(2)

for filename in camera.capture_continuous('/home/pi/Pictures/img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
    print ('Capured %s' % filename)
    periodCounter = float(18.0)
	#sleep(18)
    while (periodCounter > 0):
        while ((GPIO.input(solenoidOnOff) == True)&(periodCounter > 0)):
        #0.05s = one twentyth of a second = time solenoid energized.
            GPIO.output(solenoid, GPIO.HIGH)
            sleep(dutyCycle)
            GPIO.output(solenoid, GPIO.LOW)
            sleep((period-dutyCycle))
            periodCounter = periodCounter-period
            if (GPIO.input(solenoidOnOff) == False):
                break
        while (periodCounter > 0):
            sleep(period)
            periodCounter = periodCounter-period
            if (GPIO.input(solenoidOnOff) == True):
                break
                                