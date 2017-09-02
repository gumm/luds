from time import sleep
import RPi.GPIO as GPIO
from motors import stepper_motors

knie = stepper_motors.Sm28BJY48(con_pins=[2, 3, 4, 17], speed=0.005)
enkel = stepper_motors.Sm28BJY48(speed=0.005)

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