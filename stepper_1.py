#!/usr/bin/env python

# Target: 28BJY-48 stepper motor with ULN2003 control board.

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# CONSTANTS -----------------------------

# These are the pins corresponding to the
# stepper motor inpits.
CON_PINS = [14, 15, 18, 23]

# The step sequince
SEQ = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1],
    ]

class SM_28BJY48:
    
    # We want to keep track of the step count
    SC = 0

    # METHODS -----------------------
    def reset():
        """
        Set all pins low
        """
        for pin in CON_PINS:
            GPIO.output(pin, 0)
        
    def turn(sc, ang=360, dir=0, steps=None):
        """
        Execute stepping.
        Accepts either a number of steps, or an
        angle, and a direction.
        When given both an angle and steps, the
        angle parametr is ignored.
        When given neither steps nor an angle, one full
        rotation is executed.
        Default direction is counter-clock-wise.
        Acceps 'cw' and 'ccw' as accseptable dir values.
        Else 0 or False is counter-clock-wise or
        True or anything that evalues to true is
        considered clock-wise
        """
        
        # Parse the string values for dir
        if dir == 'cw':
            dir = 1
        if dir == 'ccw':
            dir = 0
        
        # Prepare to either count up or down
        # depending on the direction given
        counter = 1 if dir else -1
        
        # If either the steps or the angle is zero
        # there is no point in doing anything.
        if steps == 0 or ang == 0:
            return sc
        
        # When given steps, use it as is, else
        # convert the given angle to the nearest
        # integer number of steps.
        steps = steps if steps else round(ang * (512 / 360))
        
        # Depending on the given direction, rotation is either
        # a list from 0 to 7 (ccw) or 7 to 0 (cw)
        rotation = list(range(8))
        rotation = list(reversed(rotation)) if dir else rotation
        
        # Depending on the given direction, the pins are traversed either
        # from 0 to 3 (ccw) or 3 to 0 (cw)
        pins = list(range(4))
        pins = list(reversed(pins)) if dir else pins
        
        # Loop through the sequnce the required number of steps.
        # setting the GPIO output to either 1 or 0 as defined by
        # the sequnce.
        for i in range(steps):
            sc += counter
            for step in rotation:
                for pin in pins:
                    GPIO.output(CON_PINS[pin], SEQ[step][pin])
                sleep(0.001)
        reset()
        return sc

    def go_zero(v):
        """
        Return the number of steps required to get back
        to 0 if 1 rotation is 512 steps.
        The current steps may be negative or positive.
        Half rotation is 256, and this is as far as
        it is possible to get away from 0
        """
        s = v % 512
        steps = 256 - (s - 256) if s > 256 else s
        return turn(SC, steps=steps, dir=s > 256)
            


for pin in CON_PINS:
    GPIO.setup(pin, GPIO.OUT)
reset()



SC = turn(SC, dir='cw')
print(SC)

sleep(2)
print('-------------------------- RESET NOW -----')
SC = go_zero(SC)
print(SC)
GPIO.cleanup()