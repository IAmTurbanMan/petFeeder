#################################
# ADC.py			#
# module for getting ADC data	#
# and voltage conversions	#
#				#
# written by: Rash Kader	#
#	      Wesley Crank	#
#	      Na Ly		#
#	      Noah Fuji		#
#################################

#!/usr/bin/python

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as adc
from adafruit_mcp3xxx.analog_in import AnalogIn

#create objects to read ADC data
spibus = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
chip = digitalio.DigitalInOut(board.D8)
ADC = adc.MCP3008(spibus,chip)
sensor1 = AnalogIn(ADC,adc.P0)
sensor2 = AnalogIn(ADC,adc.P1)

sensorReading = 0

#function to read ADC data
#channel must be int 0 or 1 since only two sensors are being used
#on channel 0 and 1
def adcMeasure(channel):
	if channel > 1 or channel < 0:
		return -1
	if channel == 0:
		sensor_reading = sensor1.value
	if channel == 1:
		sensor_reading = sensor2.value
	return sensor_reading
