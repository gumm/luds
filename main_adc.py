from adc.ADS1115 import ADC_ADS1115
import argparse

parser = argparse.ArgumentParser(
    description='This measures angle')
parser.add_argument('-f', '--filename',
                    help='Filename to write to',
                    required=False)
parser.add_argument('-r', '--raw',
                    help='Write raw readings',
                    default=True,
                    required=False)
args = parser.parse_args()


test = ADC_ADS1115(mode_args=args)
test.run()
