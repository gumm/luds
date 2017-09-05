import argparse
from plot.plotfile import PlotFile

parser = argparse.ArgumentParser(
    description='Plot a file')
parser.add_argument('-f', '--filename', help='Write to a file', required=False)
parser.add_argument('-t', '--title', help='Give a plot title', required=False)
parser.add_argument('-s', '--start', help='Start at this time', required=False)
parser.add_argument('-e', '--end', help='End at this time', required=False)
parser.add_argument('-x', '--xLab', help='X-Axis Label', required=False)
parser.add_argument('-y', '--yLab', help='Y-Axis Label', required=False)
args = parser.parse_args()

myplot = PlotFile(mode_args=args)
myplot.draw_plot()


