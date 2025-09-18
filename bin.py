import RPi.GPIO as G
import time
G.setmode(G.BCM)
leds=[16, 12, 25,17,27,23,22,24]
G.setup(leds, G.OUT)
G.output(leds, 0)
up=9
G.setup(up, G.IN)

down=10
G.setup(down, G.OUT)
num=0
def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
while True:
    if G.input(up):
        num = num + 1
        G.output(leds[num-1], 1)
        print(num, dec2bin(num))
        time.sleep(0.2)
    if G.input(down):
        num = num - 1
        print(num, dec2bin(num))
        time.sleep(0.2)
        G.output(leds[num], 0)
