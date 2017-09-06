import multiprocessing as mp
import os
from time import sleep
import RPi.GPIO as GPIO
from motors import stepper_motors


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def motor_process(name, l, my_q, their_q, master_queue, con_pins, speed, seq, pos):
    info(name)
    motor = stepper_motors.Sm28BJY48(
        con_pins=con_pins,
        speed=speed,
        seq=seq,
        pos=pos)

    while True:
        work = my_q.get()
        if work is None:
            break
        elif work == 'STOP':
            motor.done()
            master_queue.put('%s: STOP OK' % name)
            break
        else:
            print('%s %s' % (name, work))
            f = work.pop(0)
            if f == 'turn':
                motor.turn(
                    ang=work.pop(0),
                    cw=work.pop(0),
                    steps=None,
                    duration=work.pop(0))
            elif f == 'goto':
                motor.go_to_pos(
                    work.pop(0),
                    duration=work.pop(0))
            else:
                print('%s:  I dont know what to do...' % name)
                break

            # l.acquire()
            # val = '%s sends %s' % (name, counter)
            # their_q.put(val)
            # sleep(0.5)
            # l.release()


def forward():
    knie.put(['turn', 90, True, 0.25])
    enkel.put(['turn', 40, False, 0.25])


def backward():
    knie.put(['turn', 90, False, 0.25])
    enkel.put(['turn', 40, True, 0.25])


def stride():
    forward()
    backward()


if __name__ == '__main__':
    info('main line')
    mp.set_start_method('spawn')
    main_queue = mp.Queue()
    knie = mp.Queue()
    enkel = mp.Queue()
    lock = mp.Lock()

    kp = mp.Process(target=motor_process, args=(
        'KNIE', lock, knie, enkel, main_queue,
        [6, 13, 19, 26],
        0.005,
        'DUAL_PHASE_FULL_STEP',
        20)).start()

    ep = mp.Process(target=motor_process, args=(
        'ENKEL', lock, enkel, knie, main_queue,
        [12, 16, 20, 21],
        0.005,
        'DUAL_PHASE_FULL_STEP',
        0)).start()

    sleep(1)
    print('GO!!!!')

    knie.put(['goto', 30, 0.5])

    # for i in range(2):
    #     stride()
    #     sleep(0.5)

    # Done and cleanup
    sleep(2)
    knie.put('STOP')
    print(main_queue.get())
    kp.terminate()

    enkel.put('STOP')
    print(main_queue.get())
    ep.terminate()

    print('All Done...')
    GPIO.cleanup()

