import RPi.GPIO as G
import time
G.setmode(G.BCM)
led=26
G.setup(led, G.OUT)
pwm=G.PWM(led,200)
duty=0.0
pwm.start(duty)
while True:
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    duty+=1.0
    if duty>100.0:
        duty=0.0

