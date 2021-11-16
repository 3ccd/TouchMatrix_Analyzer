import math
import threading
import time
import cv2


class TouchMatrix(threading.Thread):
    def __init__(self, mux, dec, adc):
        super().__init__(target=self.__loop)
        self.mux = mux
        self.dec = dec
        self.adc = adc
        self.interval = 0.00001
        self.framerate = 60

    def config(self, interval, framerate):
        self.interval = interval
        self.framerate = framerate

    def set_callback(self, callback):
        self.callback = callback

    def get_raw_value(self, sensor_num):
        mux_num = math.floor(sensor_num / 16)
        mux_ch = sensor_num % 16
        self.dec.set_value(mux_num)
        self.mux.set_value(mux_ch)
        time.sleep(self.interval)
        return self.adc.read()

    def __loop(self):
        while True:
            pass


