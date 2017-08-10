from gpiozero import LED, Button
from time import sleep

led_red = LED(15)
led_green = LED(18)
button = Button(2)
led_green.off()
led_red.off()
counter = 0

while True:
    button.wait_for_press()
    print(counter)
    if counter == 0:
        led_green.off()
        led_red.on()
    
    elif counter == 1:
        led_green.on()
        led_red.off()
        
    else:
        led_green.off()
        led_red.off()
        
    counter = 0 if counter == 2 else counter + 1
    sleep(0.5)
        
    
          
    
    