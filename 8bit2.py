import RPi.GPIO as G
class R2R_DAC:
    def __init__(self, leds, dynamic_range, verbose=False):
        self.leds=leds
        self.dynamic_range=dynamic_range
        self.verbose=verbose
        G.setmode(G.BCM)
        G.setup(self.leds, G.OUT, initial=0)

    def deinit(self):
        G.output(self.leds, 0)
        G.cleanup()

    def voltage_to_number(self, voltage):
        if not (0.0<=voltage<=self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} B)")
            print("Устанавливаем 0.0 В")
            return 0
        return int(voltage/ self.dynamic_range *255)
    def numder_to_dac(self, number):
        return [int(element) for element in bin(number)[2:].zfill(8)]
    def set_voltage(self, voltage):
        number=self.voltage_to_number(voltage)
        a=self.numder_to_dac(number)
        for i in range(len(a)):
            G.output(self.leds[i], a[i])
        print("Число на вход ЦАП:", self.voltage_to_number(voltage), "биты:", self.numder_to_dac(number))
if __name__=="__main__":
    try:
        dac=R2R_DAC([16,20,21,25,26,17,27,22], 3.17, True)
        while True:
            try:
                voltage=float(input("Введите число в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()