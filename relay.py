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

#define threads
#sensor1Thread = threading.Thread(target=ADC.adcMeasure, args=(0,))
#sensor2Thread = threading.Thread(target=ADC.adcMeasure, args=(1,))
#start threads
#sensor1Thread.start()
#sensor2Thread.start()

while True:
	os.system('clear')
	sensor1 = ADC.adcMeasure(0)
	sensor2 = ADC.adcMeasure(1)
#	print (waterThresh)
#	print (foodThresh)
	print (sensor1)
	print (sensor2)
	sleep(.5)
