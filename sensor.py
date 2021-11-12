import time

import spidev
import threading


class ADC(threading.Thread):
    def __init__(self, bus, ce):
        super(ADC, self).__init__(target=self.read)
        self.bus = bus
        self.ce = ce
        self.ads = spidev.SpiDev()
        self.raw = 0
        self.lock = threading.Lock()

    def open(self):
        self.ads.open(self.bus, self.ce)
        self.ads.mode = 3
        self.ads.max_speed_hz = 1000000

    def read(self):
        while True:
            byte_array = self.ads.readbytes(2)
            self.lock.acquire()
            self.raw = (byte_array[0] << 8) | byte_array[1]
            self.lock.release()
            time.sleep(0.000001)

    def get_data(self):
        self.lock.acquire()
        data = self.raw
        self.lock.release()
        return data

