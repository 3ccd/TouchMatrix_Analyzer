# coding=utf-8
import cv2
import numpy as np

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

        self.sens_img = np.ndarray()

    def start(self):
        self.tm.start()

    def imager(self, sens_array):



if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.start()

