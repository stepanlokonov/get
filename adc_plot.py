import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

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
    
    def number_to_dac(self, number):
        """Подает число number на вход ЦАП"""
        for i, pin in enumerate(self.bits_gpio):
            bit_value = (number >> i) & 1
            GPIO.output(pin, bit_value)
    
    def sequential_counting_adc(self):
        """Последовательный счетный АЦП с записью промежуточных значений"""
        max_number = (1 << len(self.bits_gpio)) - 1
        
        voltage_values = []
        time_values = []
        start_time = time.time()
        
        for number in range(max_number + 1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            
            # Записываем текущее напряжение и время
            current_time = time.time() - start_time
            current_voltage = (number / max_number) * self.dynamic_range
            
            voltage_values.append(current_voltage)
            time_values.append(current_time)
            
            comparator_state = GPIO.input(self.comp_gpio)
            
            if comparator_state == 1:
                return number, voltage_values, time_values
        
        return max_number, voltage_values, time_values
    
    def get_sc_voltage_with_progress(self):
        """Возвращает конечное напряжение и массивы промежуточных значений"""
        digital_value, voltage_progress, time_progress = self.sequential_counting_adc()
        max_digital_value = (1 << len(self.bits_gpio)) - 1
        final_voltage = (digital_value / max_digital_value) * self.dynamic_range
        return final_voltage, voltage_progress, time_progress
    
    def __del__(self):
        """Деструктор - очистка GPIO"""
        GPIO.cleanup()

def plot_voltage_vs_time(time_values, voltage_values, max_voltage):
    """Строит график зависимости напряжения от времени"""
    plt.plot(time_values, voltage_values, 'b-', linewidth=2)
    plt.title('Процесс подбора напряжения АЦП')
    plt.xlabel('Время, с')
    plt.ylabel('Напряжение, В')
    plt.grid(True)
    plt.show()

def plot_sampling_period_hist(time_values):
    """Строит распределение периодов измерений"""
    sampling_periods = []
    
    for i in range(1, len(time_values)):
        period = time_values[i] - time_values[i-1]
        sampling_periods.append(period)
    
    plt.hist(sampling_periods, bins=20, edgecolor='black', alpha=0.7)
    plt.title('Распределение периодов измерений в процессе подбора')
    plt.xlabel('Период измерения, с')
    plt.ylabel('Количество измерений')
    plt.grid(True)
    plt.show()

# Основная программа
adc = R2R_ADC(dynamic_range=3.3)

try:
    # Получаем конечное напряжение и массивы промежуточных значений
    final_voltage, voltage_progress, time_progress = adc.get_sc_voltage_with_progress()

    
  
    plot_voltage_vs_time(time_progress, voltage_progress, 3.3)
    plot_sampling_period_hist(time_progress)

finally:
    adc.__del__()