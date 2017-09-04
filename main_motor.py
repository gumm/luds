from time import sleep
import RPi.GPIO as GPIO
from motors import stepper_motors

import threading
import queue


class MotorThread(threading.Thread):

    def __init__(self, q, con_pins=None, speed=0.001, seq='HALF_STEP'):
        threading.Thread.__init__(self)

        self.q = q
        self.motor = stepper_motors.Sm28BJY48(
            con_pins=con_pins,
            speed=speed,
            seq=seq)

    def run(self):
        me = self.getName()
        print('%s is running...', me)
        while True:
            work = self.q.get()
            if work is None:
                break
            if work == 'DONE':
                print('%s:%s This is the end of me' % (me, work))
                self.q.task_done()
                return
            print('%s got this: %s' % (me, work))
            self.motor.turn(ang=work[0], cw=work(1), steps=None)
            self.q.task_done()

    def turn(self, ang=None, cw=None, steps=None):
        self.motor.turn(ang=ang, cw=cw, steps=steps)


KNIE = 90
ENKEL = 20
knie_q = queue.Queue()
enkel_q = queue.Queue()

if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    knie = MotorThread(q=knie_q, con_pins=[6, 13, 19, 26], speed=0.005, seq='DUAL_PHASE_FULL_STEP')
    enkel = MotorThread(q=enkel_q, con_pins=[12, 16, 20, 21], speed=0.005)

    knie.start()
    enkel.start()

    knie_q.put([KNIE, True])
    enkel_q.put([ENKEL, True])
    enkel_q.put([ENKEL, False])
    enkel_q.put([ENKEL, True])
    knie_q.put([KNIE, False])
    enkel_q.put([ENKEL, False])

    knie_q.put('DONE')
    enkel_q.put('DONE')
    knie.join()
    enkel.join()

    GPIO.cleanup()
    print('Done')