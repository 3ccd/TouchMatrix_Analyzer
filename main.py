# coding=utf-8

import control
import sensor
import touchmatrix


class Analyzer:
    def __init__(self):
        self.adc = sensor.ADC(0,0)
        self.mux = control.Multiplexer([6,13,19,26])
        self.dec = control.Decoder([17,27,22,23])
        self.drv = control.LEDDriver([12,16,20,21], 3, 16)
        self.tm = touchmatrix.TouchMatrix(self.mux, self.dec, self.adc, self.drv)
        print('initialize')

    def start(self):
        self.tm.set_callback(self.loop)
        self.tm.config(interval=0.8, led_count=48)
        self.tm.start()

    def loop(self, array):
        pass



if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.start()

