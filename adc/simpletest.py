# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time
from adc.ADS1115 import ADC_ADS1115

test = ADC_ADS1115()
test.run()