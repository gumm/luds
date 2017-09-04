#!/usr/bin/env python

# Target: 28BJY-48 stepper motor with ULN2003 control board.

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
    def __init__(self, con_pins=None, speed=0.001, seq='HALF_STEP'):

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
            raise ('"%s" is not a recognised step sequence name.' % seq)

        # Calculate this only once.
        self.SEQ_LENGTH = len(self.SEQ)

        # We want to keep track of the step count
        self.SC = 0

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

        return round(deg * (self.SPR / 360))
        
    def turn(self, ang=360, cw=0, steps=None):
        """
        Execute stepping.
        :param ang: A number of degrees. Defaults to 360
        :param cw: True, 1, or 'cw' for clock-wise rotation.
            False, 0, or 'ccw' for counter clockwise rotation.
            Defaults to 0 (CCW)
        :param steps: The number of steps to take. Takes precedence over the
            degrees (if both are given)
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
            return
        
        # When given steps, use it as is, else
        # convert the given angle to the nearest
        # integer number of steps.
        steps = steps if steps else self.deg_to_steps(ang)
        
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
                sleep(self.SLEEP)
        self.reset()

    def go_zero(self):
        """
        Return the number of steps required to get back
        to 0 if 1 rotation is 512 steps.
        The current steps may be negative or positive.
        Half rotation is 256, and this is as far as
        it is possible to get away from 0
        """
        halfway = int(self.SPR / 2)
        s = self.SC % self.SPR
        steps = halfway - (s - halfway) if s > halfway else s
        return self.turn(steps=steps, cw=s > halfway)
            

