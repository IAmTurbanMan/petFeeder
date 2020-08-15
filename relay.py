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
relayOn = ['off','off']
running = 'y'
sensor1 = 0
sensor2 = 0

#Relay pin setup
#Must be set up as inputs, so relays stay off
GPIO.setup(pins[0],GPIO.IN)
GPIO.setup(pins[1],GPIO.IN)

#create configparser object
config_ini = cp()
config_ini.read('./config.ini')

#function to read config.ini and return variables
#and add them to a list
def thresholds(section,setting, list):
	value = config_ini[section][setting]
	list.append(int(value))

thresholds('WATERBOWL','empty_bowl',waterThresh)
thresholds('WATERBOWL','low_water',waterThresh)
thresholds('WATERBOWL','half_full_bowl',waterThresh)
thresholds('WATERBOWL','full_bowl',waterThresh)

thresholds('FOODBOWL','empty_bowl',foodThresh)
thresholds('FOODBOWL','half_full_bowl',foodThresh)
thresholds('FOODBOWL','full_bowl',foodThresh)

#function to tell realy 1 to switch on or off depending on
#threshholds
def waterRelaySwitch():
	global sensor1, sensor2
	global relayOn, waterThresh
	while running != 'n':
		if (sensor1 < waterThresh[1] and relayOn[0] == 'off'):
			relayOn[0] = 'on'
		elif (sensor1 > waterThresh[3] and relayOn[0] == 'on'):
			relayOn[0] = 'off'

#function to poll FSRs
def polling(seconds):
	global sensor1, sensor2
	while running != 'n':
		sensor1 = ADC.adcMeasure(0)
		sensor2 = ADC.adcMeasure(1)
		sleep(seconds)

pollThread = threading.Thread(target=polling,args=(1,))
pollThread.start()
waterThread = threading.Thread(target=waterRelaySwitch)
waterThread.start()

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
