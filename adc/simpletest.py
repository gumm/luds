# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time
import argparse

# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

parser = argparse.ArgumentParser(
    description='This measures angle')
parser.add_argument('-c', '--calibrate', help='Calibrate mode', required=False)
parser.add_argument('-p', '--pin', help='The PIN to calibrate', required=False)
args = parser.parse_args()

# show values
print("Calibrate Mode: %s" % args.calibrate)
print("Calibrate PIN: %s" % args.pin)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

LOW = 1
HIGH = 26359
RANGE = HIGH - LOW

ARR = [0, 1, 2, 3]
RES = [0, 0, 0, 0]
POT_CAL = {
    0: {
        'low': 9,
        'high': 26344,
        'throw': 300
    },
    1: {
        'low': 1,
        'high': 2635,
        'throw': 300
    },
    2: {
        'low': 1,
        'high': 2635,
        'throw': 300
    },
    3: {
        'low': 1,
        'high': 2635,
        'throw': 300
    }
}


def reading_to_degrees(pin, v):
    cal = POT_CAL[pin]
    span = cal['high'] - cal['low']
    throw = cal['throw']
    return (v / span) * throw

if args.calibrate and args.pin is not None:
    # Main loop.
    while True:
        p = int(args.pin)
        v = adc.read_adc(p, gain=GAIN)
        print(v)
        time.sleep(0.1)

else:
    # Main loop.
    while True:

        # Read all the ADC channel values in a list.
        # Read the specified ADC channel using the previously set gain value.
        for p in ARR:
            RES[p] = reading_to_degrees(p, adc.read_adc(p, gain=GAIN))
        print(RES)
        time.sleep(0.1)
