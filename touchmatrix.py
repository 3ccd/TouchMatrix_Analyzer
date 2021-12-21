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
        self.led_count = 121
        self.led_enable = True

        self.buffer = []
        self.lock = threading.Lock()
        self.callback = None

        self.prev_led_num = 0

        self.warmup_count = 0
        self.warmup = 5

    def start(self) -> None:
        self.adc.open()
        super().start()

    def config(self, interval = 0.00001, led_count = 121, led_enable = True):
        self.sampling_interval = interval
        self.led_count = led_count
        self.led_enable = led_enable

    def set_callback(self, callback):
        self.callback = callback

    def get_latest_buffer(self):
        return self.buffer

    def __led(self, sens_num):
        if self.prev_led_num == sens_num: return

        self.drv.clear_buffer()
        row = int((sens_num / 11) % 2)
        self.drv.set_from_array([sens_num - 11, sens_num-row, sens_num+(1-row) , sens_num + 11], 1)
        self.drv.send_buffer()
        self.prev_led_num = sens_num

    def get_raw_value(self, sensor_num):
        mux_num = math.floor(sensor_num / 16)
        mux_ch = sensor_num % 16
        self.dec.set_value(mux_num)
        self.mux.set_value(mux_ch)
        if self.led_enable: self.__led(sensor_num)
        time.sleep(self.sampling_interval)
        return self.adc.read()

    def __loop(self):
        while True:
            array = []
            for i in range(self.led_count):
                ret = self.get_raw_value(i)
                array.append(ret)
            self.lock.acquire()
            self.buffer = array
            self.lock.release()
            if self.callback is not None and self.warmup_count > self.warmup:
                self.callback(self.buffer)
            else:
                self.warmup_count += 1
