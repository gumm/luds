import pandas as pd
import matplotlib.pyplot as plt


class PlotFile:
    def __init__(self, mode_args=None):

        self.args = mode_args
        self.title = mode_args.title
        self.read_file = mode_args.filename

        self.start = mode_args.start
        self.end = mode_args.end

        self.yLab = mode_args.yLab if mode_args.yLab else 'waarde'
        self.xLab = mode_args.xLab if mode_args.xLab else "tyd (0.05 sek stappe)"

        self.write_file = self.read_file.replace('.log', '.png')
        if self.start and self.end:
            self.write_file = self.write_file.replace(
                '.png', '_%s_%s.png' % (self.start, self.end))
            self.title = '%s - Tussen %s en %s sekondes' % (
                self.title, self.start, self.end)
        print(self.write_file)

    def calibrate_values(self):
        h = 90 / (14263 - 5282)
        k = 90 / (21935 - 13569)
        e = 90 / (21672 - 12994)
        return e, k, h

    def minmax(self):
        enkel_max = 16857
        knie_max = 21288
        heup_max = 10670

        e_min = 12654
        k_min = 14689
        h_min = 5437
        return e_min, k_min, h_min

    def draw_plot(self):
        df = pd.read_csv(
            self.read_file,
            sep=' ',
            header=None,
            usecols=[0, 1, 2, 3],
            index_col=0,
        )
        df = df.rename(
            columns={1: 'enkel', 2: 'knie', 3: 'heup'})

        if self.start and self.end:
            df = df.loc[
                (df.index >= float(self.start)) &
                (df.index <= float(self.end))
            ]

        e_min, k_min, h_min = self.minmax()
        e, k, h = self.calibrate_values()

        print(df)

        df['enkel'] = df['enkel'].apply(lambda x: x - e_min)
        df['knie'] = df['knie'].apply(lambda x: x - k_min)
        df['heup'] = df['heup'].apply(lambda x: x - h_min)
        print(df)

        df['enkel'] = df['enkel'].apply(lambda x: x * e)
        df['knie'] = df['knie'].apply(lambda x: x * k)
        df['heup'] = df['heup'].apply(lambda x: x * h)
        print(df)

        print(df.max(axis=0))
        print(df.min(axis=0))

        fig = df.plot()
        fig.set(xlabel=self.xLab, ylabel=self.yLab)
        if self.title:
            plt.title(self.title)
        # plt.show()
        plt.savefig(self.write_file)


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
