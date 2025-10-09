import RPi.GPIO as G
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin=gpio_pin
        self.pwm_frequency=pwm_frequency
        self.dynamic_range=dynamic_range
        self.verbose=verbose
        G.setmode(G.BCM)
        G.setup(self.gpio_pin, G.OUT, initial=0)

    def deinit(self):
        G.output(self.gpio_pin, 0)
        G.cleanup()

    
    def set_voltage(self, voltage):
        if not (0.0<=voltage<=self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} B)")
            print("Устанавливаем 0.0 В")
            return 0
        pwm=G.PWM(self.gpio_pin, self.pwm_frequency)
        duty=(voltage/ self.dynamic_range)*100
        pwm.start(duty)
        print("Коэффициент заполнения: ", (voltage/ self.dynamic_range)*100)
        while True:
            pwm.ChangeDutyCycle(duty)
if __name__=="__main__":
    try:
        dac=PWM_DAC(12, 500, 3.19, True)
        while True:
            try:
                voltage=float(input("Введите число в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()
