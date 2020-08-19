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
from configparser import ConfigParser as cp

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pins = [2,3]
waterThresh = []
foodThresh = []
feedingTimes = []
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
def configRead(section,setting, list):
	value = config_ini[section][setting]
	if value != '0':
		list.append(int(value))

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

def foodRelaySwitch():
	global sensor2
	global relayOn, foodThresh
	while running != 'n':
		

#function to poll FSRs
def polling(seconds,sensor):
	global sensor1, sensor2
	while running != 'n':
		if sensor == 1: sensor1 = ADC.adcMeasure(0)
		if sensor == 2: sensor2 = ADC.adcMeasure(1)
		sleep(seconds)

waterPollThread = threading.Thread(target=polling,args=(delay,1))
waterRelayThread = threading.Thread(target=waterRelaySwitch)
waterQuickPollThread = threading.Thread(target=polling,args=(.25,1))
foodQuickPollThread = threading.Thread(tarhet=polling,args=(.25,2))

waterPollThread.start()
waterRelayThread.start()

while running != 'n':
#	sensor1 = ADC.adcMeasure(0)
#	sensor2 = ADC.adcMeasure(1)
	os.system('clear')
	print (sensor1)
	print (sensor2)

	if (relayOn[0] == 'on'):
		print (relayOn[0])
		GPIO.setup(pins[0],GPIO.OUT)
	elif (relayOn[0] == 'off'):
		print (relayOn[0])
		GPIO.setup(pins[0],GPIO.IN)

	sleep(1)
