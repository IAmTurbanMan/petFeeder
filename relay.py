#################################
# relay.py			#
# relay control for pet food	#
# and water dispenser		#
#				#
# written by:	Rash Kader	#
#		Wesley Crank	#
#		Na Ly		#
#		Noah Fuji	#
#################################

#!/usr/bin/python

import os
import ADC
import threading
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime, time, timedelta
from configparser import ConfigParser as cp

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pins = [2,3]
waterThresh = []
foodThresh = []
feedingTimers = []
relayOn = ['off','off']
running = 'y'
foodRun = 'n'
sensor1 = ADC.adcMeasure(0)
sensor2 = ADC.adcMeasure(1)
delay = 0

#Relay pin setup
#Must be set up as inputs, so relays stay off
GPIO.setup(pins[0],GPIO.IN)
GPIO.setup(pins[1],GPIO.IN)

#create configparser object
config_ini = cp()
config_ini.read('./config.ini')

#function to read config.ini and return variables
#and add them to a list
def configRead(section,setting,list):
	value = config_ini[section][setting]
	if section == 'TIMING' and value != '0':
		list.append(value)
	if section != 'TIMING' and value != '0':
		list.append(int(value))

#fill lists with data from config.ini
#thresholds('WATERBOWL','empty_bowl',waterThresh)
configRead('WATERBOWL','low_water',waterThresh)
configRead('WATERBOWL','full_bowl',waterThresh)

configRead('FOODBOWL','empty_bowl',foodThresh)
configRead('FOODBOWL','full_bowl',foodThresh)

configRead('TIMING','food_timer1',feedingTimers)
configRead('TIMING','food_timer2',feedingTimers)
configRead('TIMING','food_timer3',feedingTimers)
configRead('TIMING','food_timer4',feedingTimers)

delay = int(config_ini['TIMING']['water_bowl_polling'])

format = '%I:%M%p'
minTimes = []
maxTimes = []
for x in range(len(feedingTimers)):
	minTimeObj = datetime.strptime(feedingTimers[x],format) - timedelta(minutes = 10)
	minTimes.append(minTimeObj)
	maxTimeObj = datetime.strptime(feedingTimers[x],format) + timedelta(minutes = 10)
	maxTimes.append(maxTimeObj)

minTimes = [minTimes[x].time() for x in range(len(minTimes))]
maxTimes = [maxTimes[x].time() for x in range(len(maxTimes))]

#def relayOff(relay,sensor,chan,threshold):
#	global sensor1, sensor2
#	global relayOn, foodThresh, waterThresh
#	while relay != 'off':
#		sensor = ADC.adcMeasure(chan)
#
#	if sensor >= threshold:
#		relay = 'off'

#function to turn relay1 on
def waterRelayOn():
	global sensor1
	global relayOn, waterThresh
	while running != 'n':
		if (sensor1 < waterThresh[0]):
			relayOn[0] = 'on'
			#print('on')

def waterRelayOff():
	global sensor1
	global relayOn, waterThresh
	while running != 'n':
		while (relayOn[0] == 'on'):
			sensor1 = ADC.adcMeasure(0)
			if sensor1 >= waterThresh[1]: relayOn[0] = 'off'
			else: continue

#Excellent solution that I was able to incorporate from StackOverflow user rouble
#stackoverflow.com/questions/10048249/how-do-i-determine-if-current-time-is-within-a-specified-range-using-pythons-da
#args are all datetime stamps
#checks if midnight is within range
def nowIsBetween(nowTime, minTime, maxTime):
	if minTime < maxTime:
		return nowTime >= minTime and nowTime <= maxTime
	else:
		return nowTime >= minTime or nowTime <= maxTime

#function for relay2 control
def foodRelayOn():
	global sensor2
	global relayOn, foodThresh, feedingTimers

	while running != 'n':
		now = datetime.now().time()
		for x in range (len(feedingTimers)):
			if (nowIsBetween(now, minTimes[x], maxTimes[x])):
				relayOn[1] = 'on'
		sleep (60*60)

def foodRelayOff():
	global sensor2
	global relayOn, foodThresh
	while running != 'n':
		while (relayOn[1] != 'off'):
			sensor2 = ADC.adcMeasure(1)
			if sensor2 >= foodThresh[1]: relayOn[1] = 'off'
			else: continue

#function to poll FSRs
def polling(seconds):
	global sensor1
	while running != 'n':
		sensor1 = ADC.adcMeasure(0)
#		if sensor == 2: sensor2 = ADC.adcMeasure(1)
		sleep(seconds)

#function to check relay status
def relayOnOrOff():
	global relayOn
	while running != 'n':
		if relayOn[0] == 'on':
			GPIO.setup(pins[0], GPIO.OUT)
		else:
			GPIO.setup(pins[0], GPIO.IN)

		if relayOn[1] == 'on':
			GPIO.setup(pins[1], GPIO.OUT)
		else:
			GPIO.setup(pins[1], GPIO.IN)

relayThread = threading.Thread(target=relayOnOrOff)
waterPollThread = threading.Thread(target=polling,args=(delay,))
waterRelayOnThread = threading.Thread(target=waterRelayOn)
waterRelayOffThread = threading.Thread(target=waterRelayOff)
foodRelayOnThread = threading.Thread(target=foodRelayOn)
foodRelayOffThread = threading.Thread(target=foodRelayOff)

relayThread.start()
waterPollThread.start()
waterRelayOnThread.start()
waterRelayOffThread.start()
foodRelayOnThread.start()
foodRelayOffThread.start()

x = 0
while running != 'n':
#	sensor1 = ADC.adcMeasure(0)
#	sensor2 = ADC.adcMeasure(1)

	os.system('clear')
	print (sensor1)
	print (sensor2)
	print (relayOn)
	print (waterThresh)
	print (foodThresh)
#	if (relayOn[0] == 'on' and sensor1 >= waterThresh[1]):
#		relay[0] = 'off'
#	if (relayOn[1] == 'on' and sensor2 >= foodThresh[1]):
#		relay[1] = 'off'

	sleep(1)
	x += 1

	if x == 30:
		for x in pins:
			GPIO.cleanup(x)
		running = 'n'
		exit()
