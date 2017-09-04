from time import sleep
import RPi.GPIO as GPIO
from motors import stepper_motors

import threading


class MotorThread(threading.Thread):

    def __init__(self, con_pins=None, speed=0.001, seq='HALF_STEP'):
        threading.Thread.__init__(self)

        self.motor = stepper_motors.Sm28BJY48(
            con_pins=con_pins,
            speed=speed,
            seq=seq)

    def turn(self, ang=None, cw=None, steps=None):
        self.motor.turn(ang=ang, cw=cw, steps=steps)


if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    knie = MotorThread(con_pins=[6, 13, 19, 26], speed=0.5, seq='DUAL_PHASE_FULL_STEP')
    enkel = MotorThread(con_pins=[12, 16, 20, 21], speed=0.5)

    knie.turn(ang=45, cw=True)
    enkel.turn(ang=20, cw=False)

    sleep(2)
    knie.turn(ang=45, cw=False)
    enkel.turn(ang=20, cw=True)

    # sleep(2)
    # motor.turn(ang=58, cw=False)
    # sleep(1)
    # motor.turn(ang=298, cw=True)
    # sleep(1)
    # motor.go_zero()

    GPIO.cleanup()
    print('Done')