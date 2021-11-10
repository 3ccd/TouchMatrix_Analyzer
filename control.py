import time

import RPi.GPIO as GPIO


class Decoder:
    def __init__(self, pin_array):
        if len(pin_array) < 4:
            return

        self.pin_array = pin_array

        GPIO.setmode(GPIO.BCM)
        print(self.pin_array)
        for pin in self.pin_array:
            GPIO.setup(pin, GPIO.OUT)
        self.set_enable(True)

    def set_value(self, value):
        GPIO.output(self.pin_array[2], (value & 0b00000100) >> 2)
        GPIO.output(self.pin_array[1], (value & 0b00000010) >> 1)
        GPIO.output(self.pin_array[0], value & 0b00000001)

    def set_enable(self, enable):
        GPIO.output(self.pin_array[3], enable)


class Multiplexer:
    def __init__(self, pin_array):
        if len(pin_array) < 4:
            return

        self.pin_array = pin_array

        print(self.pin_array)
        GPIO.setmode(GPIO.BCM)
        for pin in self.pin_array:
            GPIO.setup(pin, GPIO.OUT)

    def set_value(self, value):
        GPIO.output(self.pin_array[0], (value & 0b00001000) >> 3)
        GPIO.output(self.pin_array[1], (value & 0b00000100) >> 2)
        GPIO.output(self.pin_array[2], (value & 0b00000010) >> 1)
        GPIO.output(self.pin_array[3], value & 0b00000001)


class LEDDriver:
    def __init__(self, pin_array, drv_count, drv_ch):
        if len(pin_array) < 4:
            return

        self.__DRV_COUNT = drv_count
        self.__DRV_CHANNEL = drv_ch

        self.pin_array = pin_array
        self.SIN = pin_array[0]
        self.SCK = pin_array[1]
        self.RCK = pin_array[2]
        self.ENABLE = pin_array[3]

        GPIO.setmode(GPIO.BCM)
        for pin in self.pin_array:
            GPIO.setup(pin, GPIO.OUT)
        self.set_enable(True)

        self.buffer = [0] * (self.__DRV_COUNT * self.__DRV_CHANNEL)
        self.__send_buffer()

    def __shift(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        GPIO.output(pin, GPIO.LOW)

    def __send_buffer(self):
        self.set_enable(True)
        for i in range(len(self.buffer)):
            GPIO.output(self.SIN, self.buffer[i] & 0b00000001)
            self.__shift(self.SCK)
        self.__shift(self.RCK)
        self.set_enable(False)

    def set_from_array(self, array):
        for num in array:
            self.buffer[num] = 1
        self.__send_buffer()

    def test(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = 1
        self.__send_buffer()

    def clear_from_array(self, array):
        for num in array:
            self.buffer[num] = 0
        self.__send_buffer()

    def set_enable(self, enable):
        GPIO.output(self.ENABLE, enable)