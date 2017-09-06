import multiprocessing as mp
import os
from time import sleep
# import RPi.GPIO as GPIO
# from motors import stepper_motors


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def motor_process(name, l, my_q, their_q, master_queue, con_pins, speed, seq):
    info(name)
    counter = 0
    # motor = stepper_motors.Sm28BJY48(
    #     con_pins=con_pins,
    #     speed=speed,
    #     seq=seq)

    while True:
        work = my_q.get()
        if work is None:
            break
        print('%s got message from %s' % (name, work))
        counter = counter + 1
        if counter > 10:
            master_queue.put(True)
        else:
            l.acquire()
            val = '%s sends %s' % (name, counter)
            their_q.put(val)
            sleep(0.5)
            l.release()

if __name__ == '__main__':
    info('main line')
    mp.set_start_method('spawn')
    mq = mp.Queue()
    kq = mp.Queue()
    eq = mp.Queue()
    lock = mp.Lock()

    knie = mp.Process(target=motor_process, args=(
        'KNIE', lock, kq, eq, mq,
        [6, 13, 19, 26],
        0.005,
        'DUAL_PHASE_FULL_STEP'))

    enkel = mp.Process(target=motor_process, args=(
        'ENKEL', lock, eq, kq, mq,
        [12, 16, 20, 21],
        0.005,
        'DUAL_PHASE_FULL_STEP'))

    knie.start()
    enkel.start()

    sleep(5)
    print('GO!!!!')
    kq.put('GO!!!!')
    keep_going = True
    while keep_going:
        someone_is_done = mq.get()
        if someone_is_done:
            knie.terminate()
            enkel.terminate()
            keep_going = False

    print('All Done...')
