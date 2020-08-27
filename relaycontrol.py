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
sensor1 = ADC.adcMeasure(0)
sensor2 = ADC.adcMeasure(1)
delay = 0
threadsRunning = {
	'relay': False,
	'polling': False,
	'waterOn': False,
	'waterOff': False,
	'foodOn': False,
	'foodOff': False
}

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

#function to turn relay1 on
def waterRelayOn():
	global sensor1
	global relayOn, waterThresh
	while threadsRunning['waterOn']:
		if (sensor1 < waterThresh[0] and relayOn[1] != 'on'):
			relayOn[0] = 'on'
			#print('on')

#function to turn relay1 off
def waterRelayOff():
	global sensor1
	global relayOn, waterThresh
	while threadsRunning['waterOff']:
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

#function to turn relay2 on
def foodRelayOn():
	global sensor2
	global relayOn, foodThresh, feedingTimers
	while threadsRunning['foodOn']:
		now = datetime.now().time()
		for x in range (len(feedingTimers)):
			if (nowIsBetween(now, minTimes[x], maxTimes[x])):
				relayOn[1] = 'on'
		sleep (60*60)

#function to turn relay2 off
def foodRelayOff():
	global sensor2
	global relayOn, foodThresh
	while threadsRunning['foodOff']:
		while (relayOn[1] != 'off'):
			sensor2 = ADC.adcMeasure(1)
			if sensor2 >= foodThresh[1]: relayOn[1] = 'off'
			else: continue

#function to check relay status
def relayOnOrOff():
	global relayOn
	while threadsRunning['relay']:
		if relayOn[0] == 'on':
			GPIO.setup(pins[0], GPIO.OUT)
		else:
			GPIO.setup(pins[0], GPIO.IN)

		if relayOn[1] == 'on':
			GPIO.setup(pins[1], GPIO.OUT)
		else:
			GPIO.setup(pins[1], GPIO.IN)

#function to poll FSRs
def polling(seconds):
	global sensor1
	while threadsRunning['polling']:
		sensor1 = ADC.adcMeasure(0)
		sleep(seconds)


relayThread = threading.Thread(target=relayOnOrOff)
waterPollingThread = threading.Thread(target=polling,args=(delay,))
waterRelayOnThread = threading.Thread(target=waterRelayOn)
waterRelayOffThread = threading.Thread(target=waterRelayOff)
foodRelayOnThread = threading.Thread(target=foodRelayOn)
foodRelayOffThread = threading.Thread(target=foodRelayOff)

relayThread.daemon = True
waterPollingThread.daemon = True
waterRelayOnThread.daemon = True
waterRelayOffThread.daemon = True
foodRelayOnThread.daemon = True
foodRelayOffThread.daemon = True

while True:
	os.system('clear')
	print ("""
*************************
 Welcome,		*
 please make a		*
 selection.		*
			*
 1. Run program		*
 2. Exit		*
			*
*************************
	""")

	selection = input('Selection: ')
	if selection == '1':
		sensor1 = ADC.adcMeasure(0)
		sensor2 = ADC.adcMeasure(1)
		for x in threadsRunning.keys():
			threadsRunning[x] = True
		relayThread.start()
		waterPollingThread.start()
		waterRelayOnThread.start()
		waterRelayOffThread.start()
		foodRelayOnThread.start()
		foodRelayOffThread.start()
		print ('program started')
		sleep(3)

	if selection == '2':
		for x in threadsRunning.keys():
			threadsRunning[x] = False
		for x in pins:
			GPIO.cleanup(x)
		print ('exiting program')
		sleep(3)
		break
