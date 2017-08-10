#!/usr/bin/env python

# Target: 28BJY-48 stepper motor with ULN2003 control board.

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# The step sequence
SEQ = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
    ]


class StepperMotor28BJY48:
    def __init__(self, con_pins=None):

        # These are the pins corresponding to the
        # stepper motor inputs.
        self.CON_PINS = con_pins if con_pins else [14, 15, 18, 23]

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
        
    def turn(self, ang=360, direction=0, steps=None):
        """
        Execute stepping.
        Accepts either a number of steps, or an
        angle, and a direction.
        When given both an angle and steps, the
        angle parameter is ignored.
        When given neither steps nor an angle, one full
        rotation is executed.
        Default direction is counter-clock-wise.
        Accepts 'cw' and 'ccw' as acceptable dir values.
        Else 0 or False is counter-clock-wise or
        True or anything that evaluates to true is
        considered clock-wise
        """
        
        # Parse the string values for dir
        if direction == 'cw':
            direction = 1
        if direction == 'ccw':
            direction = 0
        
        # Prepare to either count up or down
        # depending on the direction given
        counter = 1 if direction else -1
        
        # If either the steps or the angle is zero
        # there is no point in doing anything.
        if steps == 0 or ang == 0:
            return
        
        # When given steps, use it as is, else
        # convert the given angle to the nearest
        # integer number of steps.
        steps = steps if steps else round(ang * (512 / 360))
        
        # Depending on the given direction, rotation is either
        # a list from 0 to 7 (ccw) or 7 to 0 (cw)
        rotation = list(range(8))
        rotation = list(reversed(rotation)) if direction else rotation
        
        # Depending on the given direction, the pins are traversed either
        # from 0 to 3 (ccw) or 3 to 0 (cw)
        pins = list(range(4))
        pins = list(reversed(pins)) if direction else pins
        
        # Loop through the sequence the required number of steps.
        # setting the GPIO output to either 1 or 0 as defined by
        # the sequence.
        for i in range(steps):
            self.SC += counter
            for step in rotation:
                for p in pins:
                    GPIO.output(self.CON_PINS[p], SEQ[step][p])
                sleep(0.001)
        self.reset()

    def go_zero(self):
        """
        Return the number of steps required to get back
        to 0 if 1 rotation is 512 steps.
        The current steps may be negative or positive.
        Half rotation is 256, and this is as far as
        it is possible to get away from 0
        """
        s = self.SC % 512
        steps = 256 - (s - 256) if s > 256 else s
        return self.turn(steps=steps, direction=s > 256)
            

motor = StepperMotor28BJY48()
motor.turn(ang=45)
sleep(2)
motor.go_zero()

GPIO.cleanup()
