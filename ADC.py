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

import spidev

#create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

#function to read SPI data from MCP3008
#channel must be int from 0-7
def adcMeasure(channel):
	if channel > 7 or channel < 0:
		return -1
	r = spi.xfer2([1, 8 + channel << 4, 0])
	data = ((r[1] & 3) << 8) + r[2]
	return data

#function to convert adc data to voltage level
#assumed voltage in = 3.3Volts
def voltageConvert(data):
	volts = (data * 3.3) / float(1023)
	volts = round(volts, 3)
	return volts
