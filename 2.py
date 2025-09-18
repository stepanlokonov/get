import RPi.GPIO as G
import time
G.setmode(G.BCM)
led=26
G.setup(led, G.OUT)
state=0
button=13
G.setup(button, G.IN)
while True:
    if G.input(button):
        state=not state
        G.output(led, state)
        time.sleep(0.2)






