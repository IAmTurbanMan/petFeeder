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

import ADC
from configparser import ConfigParser as cp
from time import sleep

#create configparser object
config_ini = cp()
config_ini.read('./config.ini')
