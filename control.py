
import RPi.GPIO as GPIO

class TMDevice:
    def __init__(self, pin_array, pin_count):
        if len(pin_array) < 4:
            return

        self.pin_array = pin_array

        GPIO.setmode(GPIO.BCM)
        print(self.pin_array)
        for pin in self.pin_array:
            GPIO.setup(pin, GPIO.OUT)

    def __del__(self):
        GPIO.cleanup()


class Decoder(TMDevice):
    def __init__(self, pin_array):
        super().__init__(pin_array, 4)
        self.set_enable(True)

    def set_value(self, value):
        GPIO.output(self.pin_array[2], (value & 0b00000100) >> 2)
        GPIO.output(self.pin_array[1], (value & 0b00000010) >> 1)
        GPIO.output(self.pin_array[0], value & 0b00000001)

    def set_enable(self, enable):
        GPIO.output(self.pin_array[3], enable)


class Multiplexer(TMDevice):
    def __init__(self, pin_array):
        super().__init__(pin_array, 4)

    def set_value(self, value):
        GPIO.output(self.pin_array[0], (value & 0b00001000) >> 3)
        GPIO.output(self.pin_array[1], (value & 0b00000100) >> 2)
        GPIO.output(self.pin_array[2], (value & 0b00000010) >> 1)
        GPIO.output(self.pin_array[3], value & 0b00000001)


class LEDDriver(TMDevice):
    def __init__(self, pin_array, drv_count, drv_ch):
        super().__init__(pin_array, 4)

        self.__DRV_COUNT = drv_count
        self.__DRV_CHANNEL = drv_ch

        self.SIN = pin_array[0]
        self.SCK = pin_array[1]
        self.RCK = pin_array[2]
        self.ENABLE = pin_array[3]

        self.set_enable(False)

        self.buffer = [0] * (self.__DRV_COUNT * self.__DRV_CHANNEL)
        self.send_buffer()

    def __shift(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        GPIO.output(pin, GPIO.LOW)

    def send_buffer(self):
        #self.set_enable(True)
        for i in range(len(self.buffer)):
            GPIO.output(self.SIN, self.buffer[(len(self.buffer) -1) - i] & 0b00000001)
            self.__shift(self.SCK)
        self.__shift(self.RCK)
        #self.set_enable(False)

    def set(self, num, enable):
        self.buffer[num] = enable & 0b00000001

    def set_from_array(self, array, enable):
        for num in array:
            if num > 0 & num <= len(self.buffer): continue
            self.buffer[num] = enable & 0b00000001

    def clear_buffer(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = 0

    def test(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = 0
        self.send_buffer()

    def set_enable(self, enable):
        GPIO.output(self.ENABLE, enable)