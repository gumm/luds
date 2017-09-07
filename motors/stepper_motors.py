#!/usr/bin/env python

# Target: 28BJY-48 stepper motor with ULN2003 control board.
import math
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Single Phase step sequence
# Fast, half resolution, low torque.
SINGLE_PHASE_STEP = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

# Dual Phase Full step sequence
# Maximum torque
# Half the resolution
# Double the speed.
DUAL_PHASE_FULL_STEP = [
    [1, 0, 0, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1]
]

# Half-step step sequence
# Maximum resolution
# Slower
# About 70% of torque
HALF_STEP = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
    ]


class Sm28BJY48:
    def __init__(self,
                 name='Sm28BJY48',
                 con_pins=None, speed=0.001,
                 seq='HALF_STEP', pos=0):
        self.name = name

        # These are the pins corresponding to the
        # stepper motor inputs.
        self.CON_PINS = con_pins if con_pins else [14, 15, 18, 23]
        self.SLEEP = speed

        if seq == 'HALF_STEP':
            self.SEQ = HALF_STEP
            self.SPR = 512
        elif seq == 'DUAL_PHASE_FULL_STEP':
            self.SEQ = DUAL_PHASE_FULL_STEP
            self.SPR = 256
        elif seq == 'SINGLE_PHASE_STEP':
            self.SEQ = SINGLE_PHASE_STEP
            self.SPR = 256
        else:
            raise Exception('"%s" is not a recognised step sequence.' % seq)

        # Calculate this only once.
        self.SEQ_LENGTH = len(self.SEQ)

        # We want to keep track of the step count
        self.SC = 0

        # We also want to keep track of the degree position
        # of the motor
        self.POS = pos

        # Degrees per step
        self.DPS = self.SPR / 360

        # Set the pins to outputs, and make them all low
        for pin in self.CON_PINS:
            GPIO.setup(pin, GPIO.OUT)
        self.reset()

    def reset(self):
        """
        Set all pins low
        """
        for p in self.CON_PINS:
            GPIO.output(p, 0)

    def deg_to_steps(self, deg):
        """
        Given some degree value, convert it to stepper motor steps
        :param deg: A number of degrees
        :return: A number of steps
        """
        if math.isnan(deg):
            return 0
        return int(round(deg * self.DPS))
        
    def turn(self, ang=360, cw=0, steps=None, duration=None):
        """
        Execute stepping.
        :param ang: A number of degrees. Defaults to 360
        :param cw: True, 1, or 'cw' for clock-wise rotation.
            False, 0, or 'ccw' for counter clockwise rotation.
            Defaults to 0 (CCW)
        :param steps: The number of steps to take. Takes precedence over the
            degrees (if both are given)
        :param duration: The amount of time (in seconds) we should take to
            execute this turn. When given we calculate the sleep time from here.
        :return:
        """
        
        # Parse the string values for dir
        if cw == 'cw':
            cw = 1
        if cw == 'ccw':
            cw = 0
        
        # Prepare to either count up or down
        # depending on the direction given
        counter = 1 if cw else -1
        
        # If either the steps or the angle is zero
        # there is no point in doing anything.
        if steps == 0 or ang == 0:
            if duration:
                sleep(duration)
            return
        
        # When given steps, use it as is, else
        # convert the given angle to the nearest
        # integer number of steps.
        steps = steps if steps else self.deg_to_steps(ang)

        # When given a time, calculate the sleep interval between steps
        if steps:
            interval = duration / steps
        else:
            interval = self.SLEEP
        interval = max(interval, 0.001)

        # Depending on the given direction, rotation is either
        # a list from 0 to self.SEQ_LENGTH (ccw) or self.SEQ_LENGTH to 0 (cw)
        rotation = list(range(self.SEQ_LENGTH))
        rotation = list(reversed(rotation)) if cw else rotation
        
        # Depending on the given direction, the pins are traversed either
        # from 0 to 3 (ccw) or 3 to 0 (cw)
        pins = list(range(4))
        pins = list(reversed(pins)) if cw else pins
        
        # Loop through the sequence the required number of steps.
        # setting the GPIO output to either 1 or 0 as defined by
        # the sequence.
        for i in range(steps):
            self.SC += counter
            for step in rotation:
                for p in pins:
                    GPIO.output(self.CON_PINS[p], self.SEQ[step][p])
                sleep(interval)

    def go_to_pos(self, target_pos, duration=None):
        delta = self.POS - target_pos
        steps = self.deg_to_steps(abs(delta))

        self.turn(ang=abs(delta), cw=(delta < 0), steps=steps, duration=duration)

        # When the delta between where we are and where we need to be
        # is very small, we may end up with 0 steps that will be taken by the
        # motor. If the then adjust our new position with the calculated delta
        # we may start to drift as a result of the rounding.
        # Address rounding drift by using the resultant steps to
        # calculate the new position, rather than simply taking the
        # given new position (p) as canon.
        sign = 1
        if delta and not math.isnan(delta):
            sign = delta / abs(delta)  # Returns 1 or -1
        calc_target = self.POS - sign * steps * self.DPS
        self.POS = calc_target
        return '%s:\tS:%s\tT:%s\tA:%s' % (
            self.name, steps, target_pos, self.POS)

    def go_to_pos_direct(self, p, duration=None):
        v = self.POS - p
        self.turn(ang=abs(v), cw=(v < 0), duration=duration)
        self.POS = p
        print('%s in pos: %s' % (self.name, self.POS))


