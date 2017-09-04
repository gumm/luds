from time import sleep
from functools import partial
import RPi.GPIO as GPIO
from motors import stepper_motors

import threading
import queue


class MotorThread(threading.Thread):

    def __init__(self, q, name, oq=None, con_pins=None, speed=0.001, seq='HALF_STEP'):
        threading.Thread.__init__(self)

        self.setName(name)
        self.q = q
        self.other_q = oq
        self.motor = stepper_motors.Sm28BJY48(
            con_pins=con_pins,
            speed=speed,
            seq=seq)

    def run(self):
        me = self.getName()
        print('%s is running...' % me)
        while True:
            work = self.q.get()
            if work is None:
                break
            if work == 'DONE':
                print('%s:%s This is the end of me' % (me, work))
                self.q.task_done()
                return
            print('%s got this: %s' % (me, work))
            self.motor.turn(
                ang=work.pop(0),
                cw=work.pop(0),
                steps=None,
                duration=0.8)
            self.q.task_done()

SPEED = 0.005
KNIE = 90
ENKEL = 20
knie_q = queue.Queue()
enkel_q = queue.Queue()


def phase_1():
    print('Phase - 1')
    enkel_q.put([10, False])
    knie_q.put([20, True])


def phase_2():
    print('Phase - 2')
    enkel_q.put([10, False])
    knie_q.put([40, True])


def phase_3():
    print('Phase - 3')
    enkel_q.put([10, True])
    knie_q.put([30, True])


def all_done():
    knie_q.put('DONE')
    enkel_q.put('DONE')
    knie.join()
    enkel.join()

    GPIO.cleanup()
    print('Done')

if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    knie = MotorThread(
        knie_q,
        'KNIE',
        oq=enkel_q,
        con_pins=[6, 13, 19, 26],
        speed=0.005,
        seq='DUAL_PHASE_FULL_STEP')
    enkel = MotorThread(
        enkel_q,
        'ENKEL',
        oq=knie_q,
        con_pins=[12, 16, 20, 21],
        speed=0.005,
        seq='DUAL_PHASE_FULL_STEP')

    knie.start()
    enkel.start()

    # phase_1()
    # phase_2()
    # phase_3()

    knie_q.put([KNIE, True])
    enkel_q.put([ENKEL, False])

    # sleep(2)
    # enkel_q.put([ENKEL, True])
    # sleep(1)
    # enkel_q.put([ENKEL, False])
    # sleep(1)

    knie_q.put([KNIE, False])
    enkel_q.put([ENKEL, True])

    all_done()
