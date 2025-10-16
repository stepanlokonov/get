import smbus
import RPi.GPIO as G
import time
import numpy as np
class MCP4725:
    def __init__(self,amplitude, address=0x61, verbose=True):
        self.bus=smbus.SMBus(1)
        self.address=address
        self.wm=0x00
        self.pds=0x00
        self.verbose=verbose
        self.amplitude=amplitude

    def deinit(self):
        self.bus.close()
    

    def set_number(self, number):
        first_bite=self.wm | self.pds | number >>8
        second_bite= number & 0xFF
        self.bus.write_byte_data(0x61, first_bite, second_bite)
        

    def set_voltage(self, voltage):
        number= int(voltage/5 * 4095)
        self.set_number(number)
    
    def sin(self, freq, time):
        return (np.sin(2*np.pi*freq*time)+1)/2
        


if __name__=="__main__":
    try:
        dac=MCP4725(5, 0x61, True)
        start=time.time()
        
        while True:
            current_time=time.time()-start
            r=dac.sin(100, current_time)+0.01
            voltage=5*r
            dac.set_voltage(voltage)
            time.sleep(1/1000)
    finally:
        dac.deinit()
