from adc.ADS1115 import ADC_ADS1115
import argparse

parser = argparse.ArgumentParser(
    description='This measures angle')
parser.add_argument('-c', '--calibrate', help='Calibrate mode', required=False)
parser.add_argument('-p', '--pin', help='The PIN to calibrate', required=False)
parser.add_argument('-f', '--filename', help='Write to a file', required=False)
args = parser.parse_args()


test = ADC_ADS1115(mode_args=args)
test.run()
