import RPi.GPIO as G
import time
import numpy as np


leds=[16,20,21,25,26,17,27,22]
G.setmode(G.BCM)
G.setup(leds, G.OUT)
G.output(leds, 0)

amplitude = 3.17
signal_frequency = 10
sampling_frequency = 100

def sin(freq, time):
    return (np.sin(2*np.pi*freq*time)+1)/2

def voltage_to_number(voltage):
    return int(voltage/ amplitude *255)
def numder_to_dac(number):
    return [int(element) for element in bin(number)[2:].zfill(8)]

def set_voltage(voltage):
    number=voltage_to_number(voltage)
    a=numder_to_dac(number)
    for i in range(len(a)):
        G.output(leds[i], a[i])

try:
    start=time.time()
    while True:
        current_time=time.time()-start
        voltage=amplitude*sin(signal_frequency, current_time)
        set_voltage(voltage)
        time.sleep(1/sampling_frequency)
finally:
    G.output(leds, 0)
    G.cleanup()
