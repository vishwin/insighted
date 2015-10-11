import time
import RPi.GPIO as GPIO
import csv
import boto3
from boto3.session import Session

GPIO.setmode(GPIO.BOARD)
switchPin=7
GPIO.setup(switchPin, GPIO.IN)
pingPin=11
timeout=0.020

with open("credentials.csv", newline='') as file:
	cred=list(csv.DictReader(file))
	session=Session(aws_access_key_id=cred[0]['Access Key Id'], aws_secret_access_key=cred[0]['Secret Access Key'], region_name='us-east-1')
dynamodb=session.resource('dynamodb')

def idle():
	while GPIO.input(switchPin)==1:
		pass
	time.sleep(1)
	return getPoints()

def getPoints():
	while GPIO.input(switchPin)==1:
		GPIO.setup(pingPin, GPIO.OUT)
		GPIO.output(pingPin, 0)
		
		time.sleep(0.000002)
		GPIO.output(pingPin, 1)
		
		time.sleep(0.000005)
		GPIO.output(pingPin, 0)
		
		GPIO.setup(pingPin, GPIO.IN)
		
		goodread=True
		watchtime=time.time()
		while GPIO.input(pingPin)==0 and goodread:
			starttime=time.time()
			if (starttime-watchtime > timeout):
				goodread=False
		
		if goodread:
			watchtime=time.time()
			while GPIO.input(pingPin)==1 and goodread:
				endtime=time.time()
				if (endtime-watchtime > timeout):
					goodread=False
		
		if goodread:
			duration=endtime-starttime
			distance=duration*34320/2 # Duration accounts for round trip
			print(distance)
	time.sleep(1)
	return idle()

idle()
