import time

# Import the ADS1x15 module.
from Adafruit_ADS1x15 import ADS1115


class ADC_ADS1115:
    def __init__(self, mode_args=None, sample_rate=0.1):

        self.args = mode_args
        self.sample_rate = sample_rate

        # Create an ADS1115 ADC (16-bit) instance.
        self.adc = ADS1115()

        # show values
        print("Calibrate Mode: %s" % self.args.calibrate)
        print("Calibrate PIN: %s" % self.args.pin)

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

    def run(self, filename=None):
        if self.args.calibrate and self.args.pin is not None:
            # Main loop.
            while True:
                p = int(self.args.pin)
                v = self.adc.read_adc(p, gain=self.GAIN)
                print(v)
                time.sleep(0.1)

        else:
            t = 0
            f = self.args.filename
            try:
                if filename:
                    f = open(filename, "w", encoding="utf-8")
                while True:
                    # # Read all the ADC channel values in a list.
                    output = '%.1f' % round(t, 1)
                    for pin, cal in self.POT_CAL.items():
                        ang = self.reading_to_degrees(
                            cal, self.adc.read_adc(pin, gain=self.GAIN))
                        output = '%s %s' % (output, ang)
                    t += self.sample_rate
                    f.write(output) if f else print(output)
                    time.sleep(self.sample_rate)
            except KeyboardInterrupt:
                f.close() if f else f







