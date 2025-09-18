import RPi.GPIO as G
import time
G.setmode(G.BCM)
led=[24,22,23,27,17,25,12,16]
leds=[16, 12, 25,17,27,23,22,24]
G.setup(led, G.OUT)
G.output(led, 0)
lght_time=0.2
for i in range(len(led)):
    G.output(led[i], 1)
    time.sleep(lght_time)
    G.output(led[i],0)
for i in range(len(leds)):
    G.output(leds[i], 1)
    time.sleep(lght_time)
    G.output(leds[i],0)

