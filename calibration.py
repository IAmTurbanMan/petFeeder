#################################
# calibration.py		#
# calibration file to run	#
# as a first time setup or 	#
# or when changing bowls.	#
#				#
# written by: Rash Kader	#
#	      Wesley Crank	#
#	      Na Ly		#
#	      Noah Fuji		#
#################################

#!/usr/bin/python

import ADC
from configparser import ConfigParser as cp
from time import sleep

#define variables and list
waterChannel = 0
foodChannel = 1
readingsList = []

#create configparser object
config_ini = cp()
config_ini.read('./config.ini')

#function to populate readingsList
#runs ADC.voltageConvert and ADC.adcMeasure to get ADC readings
#list must be list
#channel must be int from 0-7
#4 readings per second for 5 seconds
def readings (list, channel):
	for x in range (0,20):
		list.append(ADC.voltageConvert(ADC.adcMeasure(channel)))
		sleep(.25)

#function to find avg of a list of ints
def listAvg (list):
	return sum(list) / len(list)

#function to populate config.ini with average values taken from readings
#section and setting must be str
#channel must be int from 0-7
def writeConfig (channel, section, setting):
	readings(readingsList, channel)
	#print (list)
	config_ini[section][setting] = str(round(listAvg(readingsList), 4))
	readingsList.clear()

#function to commit changes to config.ini
def commitChanges():
	with open('./config.ini', 'w') as config_file:
		config_ini.write(config_file)

#function to reset config.ini settings to 0
#section and setting must be str
def resetConfig (section, setting):
	config_ini[section][setting] = '0'

#menu
selection = ''

while True:
	print('''
**********************************
 Welcome to weight calibration.  *
 please make a selection.        *
			         *
 1. Water bowl calibration       *
 2. Food bowl calibration 	 *
 3. Reset config file		 *
 4. Exit			 *
**********************************
	''')

	selection = input('Selection: ')
	if selection == '1':
		#asks user to place empty bowl on water FSR, then waits for user to press Enter
		#runs function to write avg value to config.ini file
		a = input('Please place your empty water bowl on the sensor then press Enter.')
		writeConfig(waterChannel, 'WATERBOWL', 'empty_bowl')

		#asks user to fill bowl to a low level, then waits for user to press Enter
		#same as above
		a = input('Please fill your bowl to a low level then press Enter.')
		writeConfig(waterChannel, 'WATERBOWL', 'low_water')

		#asks user to fill bowl to a half level, then waits for user to press Enter
		#same as above
		a = input('Please fill your bowl to half level then press Enter.')
		writeConfig(waterChannel, 'WATERBOWL', 'half_full_bowl')

		#asks user to fill bowl to full level, then waits for user to press Enter
		#same as above
		a = input('Please fill your bowl to full level then press Enter.')
		writeConfig(waterChannel, 'WATERBOWL', 'full_bowl')

		commitChanges()

	if selection == '2':
		#asks user to place empty bowl on food FSR, waits for user to press Enter
		#runs function to write avg value to config.ini file
		a = input('Please place your empty food bowl on the sensor then press Enter.')
		writeConfig(foodChannel, 'FOODBOWL', 'empty_bowl')

		#asks user to fill bowl half full, waits for user to press Enter
		#writes to config.ini
		a = input('Please fill your bowl to half level then press Enter.')
		writeConfig(foodChannel, 'FOODBOWL', 'half_full_bowl')

		#asks user to fill bowl to full level, waits for user to press Enter
		#writes to config.ini
		a = input('Please fill your bowl to full level then press Enter.')
		writeConfig(foodChannel, 'FOODBOWL', 'full_bowl')

		commitChanges()

	if selection == '3':
		resetConfig('WATERBOWL','empty_bowl')
		resetConfig('WATERBOWL','low_water')
		resetConfig('WATERBOWL','half_full_bowl')
		resetConfig('WATERBOWL','full_bowl')
		resetConfig('FOODBOWL','empty_bowl')
		resetConfig('FOODBOWL','half_full_bowl')
		resetConfig('FOODBOWL','full_bowl')

		commitChanges()

	if selection == '4':
		break
