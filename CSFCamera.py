import datetime;
from time import sleep
from picamera import PiCamera

camera = PiCamera()
#camera.start_preview()
sleep(2)

for filename in camera.capture_continuous('/home/pi/Pictures/img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
	print ('Capured %s' % filename)
	sleep(18)
