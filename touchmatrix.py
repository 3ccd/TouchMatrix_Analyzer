import math
import threading
import time


class TouchMatrix(threading.Thread):
    def __init__(self, mux, dec, adc):
        super().__init__(target=self.__loop)
        self.mux = mux
        self.dec = dec
        self.adc = adc
        self.sampling_interval = 0.00001
        self.framerate = 60

        self.buffer = []
        self.lock = threading.Lock()
        self.callback = None

    def start(self) -> None:
        self.adc.open()
        super().start()

    def config(self, interval, framerate):
        self.sampling_interval = interval
        self.framerate = framerate

    def set_callback(self, callback):
        self.callback = callback

    def __get_raw_value(self, sensor_num):
        mux_num = math.floor(sensor_num / 16)
        mux_ch = sensor_num % 16
        self.dec.set_value(mux_num)
        self.mux.set_value(mux_ch)
        time.sleep(self.sampling_interval)
        return self.adc.read()

    def __loop(self):
        while True:
            array = []
            for i in range(120):
                array.append(self.__get_raw_value(i))
            self.lock.acquire()
            self.buffer = array.copy()
            if self.callback is not None:
                self.callback(self.buffer)
            self.lock.release()
