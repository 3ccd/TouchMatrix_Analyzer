import math


class TouchMatrix:
    def __init__(self, mux, dec, adc):
        self.mux = mux
        self.dec = dec
        self.adc = adc

    def get_raw_value(self, sensor_num):
        mux_num = math.floor(sensor_num / 8)
        mux_ch = sensor_num % 16
        self.dec.set_value(mux_num)
        self.mux.set_value(mux_ch)
        return self.adc.get_data()