import math
import threading
import time


class TouchMatrix(threading.Thread):
    def __init__(self, mux, dec, adc, drv):
        super().__init__(target=self.__loop)
        self.mux = mux
        self.dec = dec
        self.adc = adc
        self.drv = drv

        self.sampling_interval = 0.00001
        self.framerate = 60
        self.led_count = 121

        self.buffer = []
        self.lock = threading.Lock()
        self.callback = None

    def start(self) -> None:
        self.adc.open()
        super().start()

    def config(self, interval, framerate = 30, led_count = 121):
        self.sampling_interval = interval
        self.framerate = framerate
        self.led_count = led_count

    def set_callback(self, callback):
        self.callback = callback

    def get_latest_buffer(self):
        return self.buffer

    def __led(self, sens_num):
        self.drv.clear_buffer()
        row = int((sens_num / 11) % 2)
        self.drv.set_from_array([sens_num - 11, sens_num-row, sens_num+(1-row) , sens_num + 11], 1)
        self.drv.send_buffer()

    def __get_raw_value(self, sensor_num):
        mux_num = math.floor(sensor_num / 16)
        mux_ch = sensor_num % 16
        self.dec.set_value(mux_num)
        self.mux.set_value(mux_ch)
        self.__led(sensor_num)
        time.sleep(self.sampling_interval)
        return self.adc.read()

    def __loop(self):
        while True:
            array = []
            for i in range(self.led_count-1):
                array.append(self.__get_raw_value(i))
            self.lock.acquire()
            self.buffer = array.copy()
            self.lock.release()
            if self.callback is not None:
                self.callback(self.buffer)
