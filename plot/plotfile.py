import pandas as pd
import matplotlib.pyplot as plt


class PlotFile:
    def __init__(self, mode_args=None):

        self.args = mode_args

    def draw_plot(self):
        df = pd.read_csv(self.args.filename, sep=' ', header=None)
        df.plot()
        plt.show()


# array([[ 1. ,  2. ,  3. ],
#        [ 4. ,  5.5,  6. ]])
#
# # evenly sampled time at 200ms intervals
# t = np.arange(0., 5., 0.2)
# # print(t)
#
# plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'b--')
# plt.ylabel('some numbers')
# plt.savefig("test.svg")
# plt.show()


# import matplotlib.pyplot as plt
# import numpy as np
#
# plt.figure(figsize=[6,6])
# x = np.arange(0,100,0.00001)
# y = x*np.sin(2*pi*x)
# plt.plot(y)
# plt.axis('off')
# plt.gca().set_position([0, 0, 1, 1])
