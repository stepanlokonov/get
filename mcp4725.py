import smbus
import RPi.GPIO as G
class MCP4725:
    def __init__(self,dynamic_range, address=0x61, verbose=True):
        self.bus=smbus.SMBus(1)
        self.address=address
        self.wm=0x00
        self.pds=0x00
        self.verbose=verbose
        self.dynamic_range=dynamic_range
        

    def deinit(self):
        self.bus.close()
    

    def set_number(self, number):
        if not isinstance(number, int):
            print("На выходе ЦАП можно подавать только целые числа")
        if not (0<=number<=4095):
            print("Число выходит за разрядность MCP4752(12 бит)")
        first_bite=self.wm | self.pds | number >>8
        second_bite= number & 0xFF
        self.bus.write_byte_data(0x61, first_bite, second_bite)
        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_bite:02X}, 0x{second_bite:02X}]\n")

    def set_voltage(self, voltage):
        number= int(voltage/self.dynamic_range * 4095)
        self.set_number(number)
        


if __name__=="__main__":
    try:
        dac=MCP4725(5.13, 0x61, True)
        while True:
            try:
                voltage=float(input("Введите число в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()

