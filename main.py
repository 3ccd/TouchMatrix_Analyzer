# coding=utf-8

import control
import sensor
import touchmatrix


class Analyzer:
    def __init__(self):
        self.adc = sensor.ADC(0,0)
        self.mux = control.Multiplexer([2,3,4,5])
        self.dec = control.Decoder([6,7,8,9])
        self.tm = touchmatrix.TouchMatrix(self.mux, self.dec, self.adc)
        print('initialize')

    def start(self):
        self.adc.open()
        self.adc.start()
        print(self.tm.get_raw_value(0))


if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.start()

