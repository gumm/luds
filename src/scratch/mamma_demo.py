from bluedot import BlueDot
from signal import pause

bd = BlueDot()

def move(pos):
    print(pos.angle, pos.distance)

bd.when_pressed = move
bd.when_moved = move

pause()