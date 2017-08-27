import argparse
from plot.plotfile import PlotFile

parser = argparse.ArgumentParser(
    description='Plot a file')
parser.add_argument('-f', '--filename', help='Write to a file', required=False)
args = parser.parse_args()

myplot = PlotFile(mode_args=args)
myplot.draw_plot()

