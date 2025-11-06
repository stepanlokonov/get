import time
import RPi.GPIO as GPIO

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def __del__(self):
        for pin in self.bits_gpio:
            GPIO.output(pin, 0)
        GPIO.cleanup()
    
    def number_to_dac(self, number):
        binary = format(number, '08b')  
        for i, pin in enumerate(self.bits_gpio):
            GPIO.output(pin, int(binary[i]))
    
    def sequential_counting_adc(self):
        max_number = (1 << len(self.bits_gpio)) - 1  
        
        for number in range(max_number + 1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            
            comparator_state = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"Number: {number}, Binary: {format(number, '08b')}, Comparator: {comparator_state}")
            
            if comparator_state == 1:
                return number
        
        return max_number
    
    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        max_number = (1 << len(self.bits_gpio)) - 1
        voltage = (number / max_number) * self.dynamic_range
        return voltage
    
    def successive_approximation_adc(self):
        """Алгоритм бинарного поиска напряжения на входе АЦП"""
        max_number = (1 << len(self.bits_gpio)) - 1
        number = 0
        
        # Проходим по каждому биту, начиная со старшего
        for bit in range(len(self.bits_gpio) - 1, -1, -1):
            # Устанавливаем текущий бит в 1
            test_number = number | (1 << bit)
            self.number_to_dac(test_number)
            time.sleep(self.compare_time)
            
            # Читаем состояние компаратора
            comparator_state = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"Bit {bit}: Test number {test_number} ({format(test_number, '08b')}), Comparator: {comparator_state}")
            
            # Если напряжение ЦАП меньше входного напряжения, оставляем бит установленным
            if comparator_state == 0:
                number = test_number
        
        return number
    
    def get_sar_voltage(self):
        """Возвращает измеренное алгоритмом бинарного поиска напряжение в Вольтах"""
        number = self.successive_approximation_adc()
        max_number = (1 << len(self.bits_gpio)) - 1
        voltage = (number / max_number) * self.dynamic_range
        return voltage


if __name__ == "__main__":
    try:
        # Создайте объект класса R2R_ADC, передав ему динамический диапазон вашего ЦАП
        adc = R2R_ADC(dynamic_range=3.17, verbose=False)
        
        # В бесконечном цикле делайте два действия:
        while True:
            # Читайте напряжение методом get_sar_voltage()
            voltage = adc.get_sar_voltage()
            
            # Печатайте его в терминал
            print(f"Измеренное напряжение: {voltage:.2f} В")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    finally:
        # Вызовите «деструктор» объекта класса R2R_ADC
        if 'adc' in locals():
            adc.__del__()