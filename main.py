from time import sleep
import RPi.GPIO as GPIO
from src.motors import SM_28BJY_48

motor = SM_28BJY_48.StepperMotor28BJY48()
motor.turn(ang=34, cw=True)
sleep(2)
motor.turn(ang=58, cw=False)
sleep(1)
motor.turn(ang=298, cw=True)
sleep(1)
motor.go_zero()

GPIO.cleanup()