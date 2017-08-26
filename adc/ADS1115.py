import time
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Import the ADS1x15 module.
from Adafruit_ADS1x15 import ADS1115


class ADC_ADS1115:
    def __init__(self, mode_args=None, sample_rate=0.05):

        self.args = mode_args
        self.sample_rate = sample_rate
        self.raw = self.args.raw

        # Create an ADS1115 ADC (16-bit) instance.
        self.adc = ADS1115()

        # show values
        print("Calibrate Mode: %s" % self.args.calibrate)
        print("Calibrate PIN: %s" % self.args.pin)
        if self.raw:
            print("RAW Readings")
        else:
            print('Converted readings')

        # Choose a gain of 1 for reading voltages from 0 to 4.09V.
        # Or pick a different gain to change the range of voltages that
        #  are read:
        #  - 2/3 = +/-6.144V
        #  -   1 = +/-4.096V
        #  -   2 = +/-2.048V
        #  -   4 = +/-1.024V
        #  -   8 = +/-0.512V
        #  -  16 = +/-0.256V
        # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
        self.GAIN = 1
        self.ARR = [0, 1, 2, 3]
        self.POT_CAL = {
            0: {
                'correction': 1.15,
                'offset': 30,
                'low': 9,
                'high': 26344,
                'throw': 297
            },
            1: {
                'correction': 1.15,
                'offset': 30,
                'low': 5,
                'high': 26335,
                'throw': 300
            },
            2: {
                'correction': 1.15,
                'offset': 30,
                'low': 4,
                'high': 26335,
                'throw': 300
            },
            3: {
                'correction': 1.15,
                'offset': 30,
                'low': 4,
                'high': 26335,
                'throw': 300
            }
        }

    @staticmethod
    def reading_to_degrees(cal, v):
        correction = cal['correction']
        offset = cal['offset']
        low = cal['low']
        high = cal['high']
        span = high - low
        throw = cal['throw']
        # return ((v - low) / span) * throw
        r = (((v - low) / span) * throw - offset) / correction
        return "%.2f" % round(r, 2)

    def run(self):
        if self.args.calibrate and self.args.pin is not None:
            # Main loop.
            while True:
                p = int(self.args.pin)
                v = self.adc.read_adc(p, gain=self.GAIN)
                print(v)
                time.sleep(0.1)

        else:
            t = 0
            f = None
            filename = self.args.filename
            try:
                if filename:
                    f = open(filename, "w", encoding="utf-8")
                while True:
                    # # Read all the ADC channel values in a list.
                    output = '%.2f' % round(t, 2)
                    for pin, cal in self.POT_CAL.items():
                        raw_reading = self.adc.read_adc(pin, gain=self.GAIN)
                        if self.raw:
                            ang = self.reading_to_degrees(cal, raw_reading)
                        else:
                            ang = None
                        output = '%s %s' % (output, ang if ang else raw_reading)
                    t += self.sample_rate
                    if f:
                        f.write('%s\n' % output)
                    print(output)
                    time.sleep(self.sample_rate)
            except KeyboardInterrupt:
                print('Now Plotting...')
                f.close() if f else f
                self.plot()

    def plot(self):
        filename = self.args.filename
        try:
            df = pd.read_csv(filename, sep=' ', header=None)
            del df[0]
            df.plot()
            plt.show()
        except Exception:
            print('Nothing to plot')






