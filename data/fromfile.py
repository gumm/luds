import pandas as pd
import matplotlib.pyplot as plt
from geometry import quadrilateral as quad


class DataViz:
    def __init__(self, mode_args=None):
        self.title = None
        self.start = None
        self.end = None
        self.yLab = None
        self.xLab = None
        self.write = False
        self.dps = 1
        self.motor = False
        self.motor_knie_factor = 48.8
        self.motor_enkel_factor = 60

        self.args = mode_args
        if self.args:
            self.title = self.args.title if self.args.title else 'Title'
            self.read_file = self.args.filename

            self.start = self.args.start
            self.end = self.args.end

            self.yLab = self.args.yLab if self.args.yLab else 'waarde'
            self.xLab = self.args.xLab if self.args.xLab else "tyd (0.05 sek stappe)"

            self.write = self.args.write
            self.dps = float(self.args.dps)

            self.motor = self.args.motor
            if self.motor and self.dps == 1:
                self.dps = 0.01

            if self.start and self.end:
                self.title = '%s - Tussen %s en %s sekondes' % (
                    self.title, self.start, self.end)

    def quad(self, n, col, adjust):
        v = n + adjust
        try:
            res = quad.mb_mfb(v, col)
        except AssertionError:
            res = None
        return res

    def get_normal(self, df, col, adjust):
        return df[col].min(axis=0) + adjust

    def clean_data(self):
        knie = 'knie'
        enkel = 'enkel'
        heup = 'heup'

        df = pd.read_csv(
            self.read_file,
            sep=' ',
            header=None,
            usecols=[0, 1, 2, 3],
            index_col=0,
        )
        df = df.rename(
            columns={1: enkel, 2: knie, 3: heup})

        if self.start and self.end:
            df = df.loc[
                (df.index >= float(self.start)) &
                (df.index <= float(self.end))
                ]

        # Grab in and max values for each measurement
        # Because both heup and enkel bends in both directions from the
        # "standing" position, we can not simply rely on their minimum values
        # to get to their "normal" positions, but need to further adjust those
        # with a factor, to get all the "standing" data to line up
        k_nor = self.get_normal(df, knie, 500)
        e_nor = self.get_normal(df, enkel, 900)
        h_nor = self.get_normal(df, heup, 200)

        # Normalise the measurements
        df[enkel] = df[enkel].apply(lambda x: x - e_nor)
        df[knie] = df[knie].apply(lambda x: x - k_nor)
        df[heup] = df[heup].apply(lambda x: x - h_nor)

        # Convert all measurements using the same DPS factor
        # This converts the digital reading to degrees
        if self.dps is not 1:
            df = df.apply(lambda x: x * self.dps)

        # Calculate the required motor positions for each of the joints
        if self.motor:
            df[enkel] = df[enkel].apply(
                lambda x: self.quad(x, enkel, self.motor_enkel_factor))
            df[knie] = df[knie].apply(
                lambda x: self.quad(x, knie, self.motor_knie_factor))
        return df

    def go(self):
        if self.write:
            self.save_plot()
        else:
            self.show_plot()

    def draw_plot(self):
        df = self.clean_data()
        print(df)

        fig = df.plot()
        fig.set(xlabel=self.xLab, ylabel=self.yLab)
        if self.title:
            plt.title(self.title)
        return plt

    def get_data(self, filename, dps=0.01, knie=48.8, enkel=60):
        self.read_file = filename
        self.dps = dps
        self.motor_knie_factor = knie
        self.motor_enkel_factor = enkel
        self.motor = True

        df = self.clean_data()
        return [tuple(x) for x in df.values]

    def save_plot(self):
        self.draw_plot().savefig('%s.png' % self.title)

    def show_plot(self):
        self.draw_plot().show()
