import RPi.GPIO as G
G.setmode(G.BCM)
led=23
G.setup(led, G.OUT)
G.output(led, 0)
p=6
G.setup(led, G.OUT)
G.setup(p, G.IN)
while True:
    if G.input(p)==1:
        G.output(led,0)
    else:
        G.output(led, 1)
