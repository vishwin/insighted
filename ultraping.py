import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

timeout=0.020

while 1:
	GPIO.setup(11, GPIO.OUT)
	GPIO.output(11, 0)
	
	time.sleep(0.000002)
	GPIO.output(11, 1)
	
	time.sleep(0.000005)
	GPIO.output(11, 0)
	
	GPIO.setup(11, GPIO.IN)
	
	goodread=True
	watchtime=time.time()
	while GPIO.input(11)==0 and goodread:
		starttime=time.time()
		if (starttime-watchtime > timeout):
			goodread=False
	
	if goodread:
		watchtime=time.time()
		while GPIO.input(11)==1 and goodread:
			endtime=time.time()
			if (endtime-watchtime > timeout):
				goodread=False
	
	if goodread:
		duration=endtime-starttime
		distance=duration*34000/2
		print(distance)
