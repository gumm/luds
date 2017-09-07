import multiprocessing as mp
from multiprocessing import Process, Pipe, Queue
import os
from time import sleep
import RPi.GPIO as GPIO
from motors import stepper_motors


#   enkel   knie    heup
DD = [
    [8.18,  0.00, 50.17],
    [8.32,  4.53, 52.44],
    [8.41, 14.82, 51.49],
    [8.47, 27.42, 46.39],
    [8.44, 35.12, 41.33],
    [8.43, 38.06, 37.89],
    [8.24, 39.28, 36.05],
    [7.39, 40.50, 35.95],
    [6.51, 38.10, 35.79],
    [6.73, 37.98, 35.92],
    [7.31, 38.09, 36.29],
    [7.55, 38.89, 35.89],
    [7.71, 39.35, 33.67],
    [7.75, 40.16, 32.67],
    [7.87, 40.51, 31.89],
    [7.90, 40.95, 28.28],
    [7.91, 41.65, 24.33],
    [7.73, 42.14, 20.50],
    [7.51, 42.15, 17.37],
    [7.36, 42.03, 14.61],
    [7.21, 41.30, 12.04],
    [7.23, 41.33,  6.52],
    [7.37, 41.73,  4.25],
    [7.30, 41.84,  3.91],
    [7.20, 41.70,  2.12],
    [7.19, 41.51,  0.00],
    [7.49, 39.34,  8.29],
    [7.49, 39.34, 8.29],
    [5.73, 38.40, 6.63],
    [3.58, 37.95, 4.62],
    [1.66, 37.28, 4.19],
    [0.19, 35.44, 3.49],
    [0.00, 32.28, 3.47],
    [0.30, 25.31, 6.31],
    [4.04, 16.90, 12.87],
    [5.35, 11.86, 21.15],
    [6.90, 7.02, 32.16],
    [7.64, 1.39, 43.34],
    [8.18,  0.00, 50.17],
]


def motor_process(name, my_q, my_pipe, con_pins, speed, seq, pos):
    motor = stepper_motors.Sm28BJY48(
        name=name,
        con_pins=con_pins,
        speed=speed,
        seq=seq,
        pos=pos)

    while True:
        work = my_q.get()
        if work is None:
            break
        elif work == 'STOP':
            motor.reset()
            my_pipe.send('%s: STOP OK' % name)
            return
        else:
            f = work.pop(0)
            if f == 'goto':
                motor.go_to_pos(
                    work.pop(0),
                    duration=work.pop(0))
                my_pipe.send('%s OK' % name)
            else:
                print('%s:  I dont know what to do with:' % (name, f))
                break


if __name__ == '__main__':
    mp.set_start_method('spawn')
    knie_recv, knie_send = Pipe(duplex=False)
    enkel_recv, enkel_send = Pipe(duplex=False)
    knie = Queue()
    enkel = Queue()

    kp = Process(target=motor_process, args=(
        'KNIE', knie, knie_send,
        [6, 13, 19, 26],
        0.001,
        'DUAL_PHASE_FULL_STEP',
        39.34)).start()

    ep = Process(target=motor_process, args=(
        'ENKEL', enkel, enkel_send,
        [12, 16, 20, 21],
        0.001,
        'DUAL_PHASE_FULL_STEP',
        7.49)).start()

    sleep(1)
    print('GO!!!!')

    SPEED = 0.015
    for i in range(5):
        for d in DD:
            knie.put(['goto', d[1], SPEED])
            enkel.put(['goto', d[0], SPEED])
            print(knie_recv.recv())
            print(enkel_recv.recv())

    # Done and cleanup
    sleep(2)
    knie.put('STOP')
    print(knie_recv.recv())

    enkel.put('STOP')
    print(enkel_recv.recv())

    GPIO.cleanup()
    print('GPIO Cleanup Done...')
