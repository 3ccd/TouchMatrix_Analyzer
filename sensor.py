import spidev


class ADC:
    def __init__(self, bus, ce):
        self.bus = bus
        self.ce = ce
        self.ads = spidev.SpiDev()
        self.raw = 0

    def open(self):
        self.ads.open(self.bus, self.ce)
        self.ads.mode = 3
        self.ads.max_speed_hz = 1000000

    def read(self):
        byte_array = self.ads.readbytes(2)
        byte_array = self.ads.readbytes(2)
        self.raw = (byte_array[0] << 8) | byte_array[1]
        return self.raw
