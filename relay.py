#################################
# relay.pi			#
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
sensor1 = 0
sensor2 = 0
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

delay = config_ini['TIMING']['water_bowl_polling']

#function to tell realy 1 to switch on or off depending on
#threshholds
def waterRelaySwitch():
	global sensor1
	global relayOn, waterThresh
	while running != 'n':
		if (sensor1 < waterThresh[1] and relayOn[0] == 'off'):
			relayOn[0] = 'on'
			waterQuickPollThread.start()
		elif (sensor1 > waterThresh[3] and relayOn[0] == 'on'):
			relayOn[0] = 'off'
			waterQuickPollThread.join()

def timeParsing(string):
	x = datetime.strptime(string,'%I:%M%p')
	return x

#Excellent solution that I was able to incorporate from StackOverflow user rouble
#stackoverflow.com/questions/10048249/how-do-i-determine-if-current-time-is-within-a-specified-range-using-pythons-da
#args are all datetime stamps
def nowIsBetween(nowTime, minTime, maxTime):
	if minTime < maxTime:
		return nowTime >= minTime and nowTime <= maxTime
	else:
		return nowTime >= minTime or nowTime <= maxTime


def foodRelaySwitch():
	global sensor2
	global relayOn, foodThresh, feedingTimers
	minTimes = []
	maxTimes = []
	for x in range(len(feedingTimers)):
		minTimeObj = timeParsing(feedingTimers[x]) - timedelta(minutes = 10)
		minTimes.append(minTimeObj)
		maxTimeObj = timeParsing(feedingTimers[x]) + timedelta(minutes = 10)
		maxTimes.append(maxTimeObj)

	minTimes = [minTimes[x].time() for x in range(len(minTimes))]
	maxTimes = [maxTimes[x].time() for x in range(len(maxTimes))]

	while running != 'n':
		now = datetime.now().time()
		for x in range (len(feedingTimers)):
			if (nowIsBetween(now, minTimes[x], maxTimes[x]) and relay[1] == 'off'): 
				relayOn[1] = 'on'
				foodQuickPollThread.start()
				if sensor2 > foodThresh[1]:
					relayOn[1] == 'off'
					foodQuickPollThread.join()
		sleep (60)

#function to check relay status
def relayOnOrOff():
	if relayOn[0] == 'on':
		print (relayOn[0])
		GPIO.setup(pins[0], GPIO.OUT)
	if relayOn[1] == 'on':
		print (relayOn[1])
		GPIO.setup(pins[1], GPIO.OUT)
	if relayOn[0] == 'off':
		print (relayOn[0])
		GPIO.setup(pins[0], GPIO.IN)
	if relayOn[0] == 'off':
		print (relayOn[1])
		GPIO.setup(pins[1], GPIO.OUT)

#function to poll FSRs
def polling(seconds,sensor):
	global sensor1, sensor2
	while running != 'n':
		if sensor == 1: sensor1 = ADC.adcMeasure(0)
		if sensor == 2: sensor2 = ADC.adcMeasure(1)
		sleep(seconds)

relayThread = threading.Thread(target=relayOnOrOff)
waterPollThread = threading.Thread(target=polling,args=(delay,1))
waterRelayThread = threading.Thread(target=waterRelaySwitch)
foodRelayThread = threading.Thread(target = foodRelaySwitch)
waterQuickPollThread = threading.Thread(target=polling,args=(.25,1))
foodQuickPollThread = threading.Thread(target=polling,args=(.25,2))

relayThread.start()
waterPollThread.start()
waterRelayThread.start()
foodRelayThread.start()

x = 0
while running != 'n':
#	sensor1 = ADC.adcMeasure(0)
#	sensor2 = ADC.adcMeasure(1)
	os.system('clear')
	print (sensor1)
	print (sensor2)

#	if (relayOn[0] == 'on'):
#		print (relayOn[0])
#		GPIO.setup(pins[0],GPIO.OUT)
#	elif (relayOn[0] == 'off'):
#		print (relayOn[0])
#		GPIO.setup(pins[0],GPIO.IN)
#
	sleep(1)
	x += 1

	if x == 10:
		for x in pins:
			GPIO.cleanup(x)
