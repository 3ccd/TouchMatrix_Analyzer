import RPi.GPIO as GPIO


class Decoder:
    def __init__(self, pin_array):
        if len(pin_array) < 4:
            return

        self.pin_array = pin_array

        GPIO.setmode(GPIO.BCM)
        for pin in self.pin_array:
            GPIO.setup(pin, GPIO.OUT)
        self.set_enable(True)

    def set_value(self, value):
        GPIO.output(self.pin_array[0], (value & 0b00000100) >> 2)
        GPIO.output(self.pin_array[1], (value & 0b00000010) >> 1)
        GPIO.output(self.pin_array[2], value & 0b00000001)

    def set_enable(self, enable):
        GPIO.output(self.pin_array[3], enable)


class Multiplexer:
    def __init__(self, pin_array):
        if len(pin_array) < 4:
            return

        self.pin_array = pin_array

        GPIO.setmode(GPIO.BCM)
        for pin in self.pin_array:
            GPIO.setup(pin, GPIO.OUT)

    def set_value(self, value):
        GPIO.output(self.pin_array[0], (value & 0b00001000) >> 3)
        GPIO.output(self.pin_array[1], (value & 0b00000100) >> 2)
        GPIO.output(self.pin_array[2], (value & 0b00000010) >> 1)
        GPIO.output(self.pin_array[3], value & 0b00000001)