#################################
# calibration.py		#
# calibration file to run	#
# as a first time setup or 	#
# or when changing bowls.	#
# built in data redundancy	#
# with json file in case 	#
# of data loss			#
#				#
# written by: Rash Kader	#
#	      Wesley Crank	#
#	      Na Ly		#
#	      Noah Fuji		#
#################################

#!/usr/bin/python
import os
import ADC
import datetime
from time import sleep
from configparser import ConfigParser as cp

#define global variables
avg = 0
channel = 0
section = ''
selection = ''
readingsList = []
feedingTimes = ['0','0','0','0']

#create configparser object
config_ini = cp()
config_ini.read('./config.ini')

#function to populate readingsList
#runs ADC.adcMeasure to get ADC readings
#channel must be int from 0-1
#10 readings per second for 5 seconds
def readings (channel):
	global readingsList
	for x in range (0,50):
		readingsList.append(ADC.adcMeasure(channel))
		sleep(.1)

#function to find avg of a list of ints
def listAvg (list):
	return sum(list) / len(list)

#function to write values to config.ini
#section and setting must be str
def writeConfig (section, setting, value):
	config_ini[section][setting] = str(value)

#function to commit changes to config.ini
def commitChanges():
	with open('./config.ini', 'w') as config_file:
		config_ini.write(config_file)

#function for use in setting feeding times
#loops message with approprite wording
#asks for time in %I:%M%p format
#makes any necessary conversions in timeStr to match time format
#replaces default value '0' in feedingTime
def messageLoop(n):
	global feedingTimes
	nth = ''
	timeStr = ''
	x = 0
	for y in range (0,n):
		os.system('clear')
		if x == 0: nth = 'first'
		if x == 1: nth = 'second'
		if x == 2: nth = 'third'
		if x == 3: nth = 'fourth'
		print ("""
**********************************
 Enter the {} time		 *
 Format: HH:MMpm		 *
				 *
**********************************
		""".format(nth))
		timeStr = input('Time: ')
		timeStr = timeStr.replace(' ','')
		timeStr = timeStr.upper()
		feedingTimes[x] = timeStr
		x += 1

#function to reset config.ini settings to 0
#section and setting must be str
def resetConfig (section, setting):
	config_ini[section][setting] = '0'

def clear():
	os.system('clear')

def menu():
	global selection
	clear()
	print('''
**********************************
 Welcome to weight calibration.  *
 please make a selection.        *
			         *
 1. Water bowl calibration       *
 2. Food bowl calibration 	 *
 3. Enter timing information	 *
 4. Reset config file		 *
 5. Exit			 *
**********************************
	''')
	selection = input('Selection: ')
#menu
while selection != '5':

	menu()
	if selection == '1':
		section = 'WATERBOWL'
		channel = 0
		#asks user to place empty bowl on water FSR, then waits for user to press Enter
		#runs function to write avg value to config.ini file
		a = input('Please place your empty water bowl on the sensor then press Enter.')
		readings(channel)
		avg = int(listAvg(readingsList))
		writeConfig(section, 'empty_bowl', avg)
		readingsList.clear()

		#asks user to fill bowl to a low level, then waits for user to press Enter
		#same as above
		a = input('Please fill your bowl to a low level then press Enter.')
		readings(channel)
		avg = int(listAvg(readingsList))
		writeConfig(section, 'low_water', avg)
		readingsList.clear()

		#asks user to fill bowl to full level, then waits for user to press Enter
		#same as above
		a = input('Please fill your bowl to full level then press Enter.')
		readings(channel)
		avg = int(listAvg(readingsList))
		writeConfig(section, 'full_bowl', avg)
		readingsList.clear()

		commitChanges()

	if selection == '2':
		section = 'FOODBOWL'
		channel = 1
		#asks user to place empty bowl on food FSR, waits for user to press Enter
		#runs function to write avg value to config.ini file
		a = input('Please place your empty food bowl on the sensor then press Enter.')
		readings(channel)
		avg = int(listAvg(readingsList))
		writeConfig(section, 'empty_bowl', avg)
		readingsList.clear()

		#asks user to fill bowl to full level, waits for user to press Enter
		#writes to config.ini
		a = input('Please fill your bowl to full level then press Enter.')
		readings(channel)
		avg = int(listAvg(readingsList))
		writeConfig(section, 'full_bowl', avg)
		readingsList.clear()

		commitChanges()

	if selection == '3':
		clear()
		section = 'TIMING'
		print ("""
**********************************
 How often would you like the	 *
 system to check the water level?*
				 *
**********************************
 		""")
		time = int(input('Minutes: '))
		time = time * 60
		writeConfig(section,'water_bowl_polling',time)
		sleep(.5)
		os.system('clear')

		print ("""
**********************************
 How many times per day would 	 *
 you like the feeder to run?	 *
				 *
**********************************
		""")
		n = int(input('1-4: '))

#		while (n < 1 or n > 4):
#			n = int(input('please enter a number between 1 and 4: ')

		messageLoop(n)
		y = 0
		for x in feedingTimes:
			setting = ''
			if y == 0: setting = 'food_timer1'
			if y == 1: setting = 'food_timer2'
			if y == 2: setting = 'food_timer3'
			if y == 3: setting = 'food_timer4'
			writeConfig(section,setting,feedingTimes[y])
			y += 1

		commitChanges()

	if selection == '4':
		clear()
		resetConfig('WATERBOWL','empty_bowl')
		resetConfig('WATERBOWL','low_water')
		resetConfig('WATERBOWL','full_bowl')
		resetConfig('FOODBOWL','empty_bowl')
		resetConfig('FOODBOWL','full_bowl')
		resetConfig('TIMING','water_bowl_polling')
		resetConfig('TIMING','food_timer1')
		resetConfig('TIMING','food_timer2')
		resetConfig('TIMING','food_timer3')
		resetConfig('TIMING','food_timer3')
		print ('config.ini reset to defaults')

		commitChanges()
