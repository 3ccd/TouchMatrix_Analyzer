# coding=utf-8

import control
import sensor
import touchmatrix
import time
import math

import cv2
import numpy as np


class Analyzer:

    def __init__(self):
        self.adc = sensor.ADC(0,0)
        self.mux = control.Multiplexer([6,13,19,26])
        self.dec = control.Decoder([17,27,22,23])
        self.drv = control.LEDDriver([12,16,20,21], 8, 16)
        self.tm = touchmatrix.TouchMatrix(self.mux, self.dec, self.adc, self.drv)

        self.led_insert_pos = self.insert_led()
        print(self.led_insert_pos)
        print(len(self.led_insert_pos))
        print('initialize')

    def test(self):
        self.adc.open()
        print('start')
        time.sleep(1)
        n_array = np.array([0.0,0.0,0.0]).reshape(1,3)
        start = time.time()
        while True:
            elapsed_time = time.time() - start
            tmp = np.array([elapsed_time, self.tm.get_raw_value(53), self.tm.get_raw_value(75)]).reshape(1,3)
            n_array = np.append(n_array, tmp, axis=0)
            time.sleep(0.001)
            if elapsed_time > 3.0:
                break
        np.savetxt('./np_savetxt_clear.csv', n_array, delimiter=',', fmt='%f')

    def insert_led(self):
        pos = []
        for i in range(11):
            pos.extend(range((i % 2) + (i * 11), (i+1) * 11 + (i % 2), 1))
        return pos

    def start(self):
        self.tm.set_callback(self.loop)
        self.tm.start()

    def loop(self, array):
        n_array = pow((np.array(array, "u2") / 65536 ) , 3) * 255
        n_array = np.insert(n_array, self.led_insert_pos, 0)
        n_array = np.reshape(n_array, (11,22))
        img3 = cv2.resize(n_array, (int(22 * 30), int(11 * 30)), interpolation = cv2.INTER_NEAREST)
        cv2.imshow('ir', img3)
        cv2.waitKey(1)
        #print(n_array)

    def detect_error(self, array):
        err_arr = []
        for i in range(len(array)):
            if array[i] == 0:
                err_arr.append(i)
        print(err_arr)


if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.start()
    #analyzer.test()

