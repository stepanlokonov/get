import RPi.GPIO as G
leds=[16,20,21,25,26,17,27,22]
G.setmode(G.BCM)
G.setup(leds, G.OUT)
G.output(leds, 0)
dynamic_range=3.17
def voltage_to_number(voltage):
    if not (0.0<=voltage<=dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} B)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage/ dynamic_range *255)
def numder_to_dac(number):
    return [int(element) for element in bin(number)[2:].zfill(8)]

try:
    while True:
        try:
            voltage=float(input("Введите напряжение в вольтах: "))
            number=voltage_to_number(voltage)
            a=numder_to_dac(number)
            for i in range(len(a)):
                G.output(leds[i], a[i])
            print("Число на вход ЦАП:", voltage_to_number(voltage), "биты:", numder_to_dac(number))
        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")
finally:
    G.output(leds, 0)
    G.cleanup()
    
