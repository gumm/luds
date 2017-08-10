import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class LED:
    
    def __init__(self, bcm=18, hz=3, color=''):
        self.GP_PIN_NUM = bcm
        self.FREQ = hz
        self.color = color
        GPIO.setup(self.GP_PIN_NUM, GPIO.OUT)

    def on(self):
        GPIO.output(self.GP_PIN_NUM, GPIO.HIGH)
        
    def off(self):
        GPIO.output(self.GP_PIN_NUM, GPIO.LOW)
        
    def flash_pwm(self):
        p = GPIO.PWM(self.GP_PIN_NUM, self.FREQ)
        duty_cycle = 10
        p.start(duty_cycle)
        input('Press return to stop:')   # use raw_input for Python 2
        p.stop()
        GPIO.cleanup()
        
    def bd(self):
        p = GPIO.PWM(self.GP_PIN_NUM, 50)  # channel=12 frequency=50Hz
        p.start(0)
        try:
            while 1:
                for dc in range(0, 101, 5):
                    p.ChangeDutyCycle(dc)
                    time.sleep(0.1)
                for dc in range(100, -1, -5):
                    p.ChangeDutyCycle(dc)
                    time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        p.stop()
        GPIO.cleanup()
        
    def flash_n_at_freq(self, n, hz=None):
        """
        Flash the LED n times in t seconds.
        It is guarenteed to end with the LED off.
        :param n: How many times to flash
        :param t: Time in seconds to produce the flashes
        """
        freq = hz if hz else self.FREQ
        print("%s: Flashing %s times at %s hertz" % (self.color, n, freq))
        sleep_time = (1 / freq) / 2
        for a in range(0, n):
            self.on()
            time.sleep(sleep_time)
            self.off()
            time.sleep(sleep_time)  
            
    def flash(self, n):
        if n:
            self.flash_n_at_freq(n)
        

def cleanup():
    GPIO.cleanup()