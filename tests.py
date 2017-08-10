import time
import led

red = led.LED(bcm=18, hz=2.5, color="RED")
green = led.LED(bcm=23, hz=2.5, color="GREEN")

green.off()
red.off()

# green.bd()

for a in range(2):
   red.flash(a)
   green.flash(a)
   time.sleep(1)
    
red.on()
green.flash_n_at_freq(30, hz=10)

green.off()

led.cleanup()

