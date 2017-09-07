import argparse
from data.fromfile import DataViz

parser = argparse.ArgumentParser(
    description='Plot a file')

parser.add_argument('-f', '--filename',
                    help='File to read from', required=False)
parser.add_argument('-t', '--title',
                    help='Give a plot title', required=False)
parser.add_argument('-s', '--start',
                    help='Start at this time', required=False)
parser.add_argument('-e', '--end',
                    help='End at this time', required=False)
parser.add_argument('-x', '--xLab',
                    help='X-Axis Label', required=False)
parser.add_argument('-y', '--yLab',
                    help='Y-Axis Label', required=False)
parser.add_argument('-w', '--write',
                    help='Write to file', required=False)
parser.add_argument('-d', '--dps',
                    help='The DPS conversion factor that converts the'
                         'digital readings to human readable degrees. '
                         'Should be around 0.01. Adjust this upwards to '
                         'amplify the gait, or down to smooth it out.',
                    default=1, required=False)
parser.add_argument('-m', '--motor',
                    help='Geometrically convert the values to the '
                         'motor driver values. When set to true, it requires a'
                         'DPS value, and will use 0.01 if the -d flag was '
                         'not set',
                    default=False,
                    required=False)
args = parser.parse_args()

my_data_viz = DataViz(mode_args=args)
my_data_viz.go()


