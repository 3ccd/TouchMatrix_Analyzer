# coding=utf-8
import time

import control
import sensor
import touchmatrix


class Analyzer:
    def __init__(self):
        self.adc = sensor.ADC(0,0)
        self.mux = control.Multiplexer([6,13,19,26])
        self.dec = control.Decoder([17,27,22,23])
        self.drv = control.LEDDriver([12,16,20,21], 1, 16)
        self.tm = touchmatrix.TouchMatrix(self.mux, self.dec, self.adc)
        print('initialize')

    def start(self):
        self.adc.open()
        self.adc.start()
        while True:
            array = []
            for i in range(32):
                array.append(self.tm.get_raw_value(i))
            print(array)
            self.drv.test()
            time.sleep(0.5)


if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.start()

