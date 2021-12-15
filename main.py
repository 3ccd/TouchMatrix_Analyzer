# coding=utf-8
import sys

import control
import sensor
import touchmatrix
import time
import math

import cv2
import numpy as np

import RPi.GPIO as GPIO


class Analyzer:
    CAL_MAX = 2
    CAL_MIN = 1

    def __init__(self):
        self.adc = sensor.ADC(0,0)
        self.mux = control.Multiplexer([6,13,19,26])
        self.dec = control.Decoder([17,27,22,23])
        self.drv = control.LEDDriver([12,16,20,21], 8, 16)
        self.tm = touchmatrix.TouchMatrix(self.mux, self.dec, self.adc, self.drv)

        self.cal_state = 0
        self.cal_max = None
        self.cal_min = None

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

    def test_2(self):
        GPIO.setup(14, GPIO.OUT)
        self.adc.open()
        print('start')
        time.sleep(1)
        n_array = np.array([0.0,0.0]).reshape(1,2)
        start = time.time()
        while True:
            elapsed_time = time.time() - start
            tmp = np.array([elapsed_time, self.tm.get_raw_value(74)]).reshape(1,2)
            n_array = np.append(n_array, tmp, axis=0)
            time.sleep(0.001)
            if elapsed_time > 4.0:
                break
            elif elapsed_time > 2.0:
                GPIO.output(14, GPIO.LOW)
            elif elapsed_time > 0.0:
                GPIO.output(14, GPIO.HIGH)

        np.savetxt('./np_savetxt_touch_'+str(time.time())+'.csv', n_array, delimiter=',', fmt='%f')

    def insert_led(self):
        pos = []
        for i in range(11):
            pos.extend(range((i % 2) + (i * 11), (i+1) * 11 + (i % 2), 1))
        return pos

    def start(self):
        self.tm.set_callback(self.loop)
        self.tm.start()

    def __calibration(self, data):
        if self.cal_state < self.CAL_MIN:
            print('calibrate min')
            self.cal_min = data
            print(data)
            self.cal_state = self.CAL_MIN
            input()
            return
        if self.cal_state < self.CAL_MAX:
            print('calibrate max')
            self.cal_max = data
            print(data)
            self.range = self.cal_max - self.cal_min
            #self.range[self.range < 0] = 0
            print(self.range)
            self.cal_state = self.CAL_MAX
            return


    def loop(self, array):
        data = np.array(array, np.uint16)

        self.__calibration(data)
        if self.cal_min is not None and self.cal_max is not None:
            data[data <= self.cal_min] = self.cal_min[data <= self.cal_min]
            offset = data - self.cal_min

            offset[offset >= self.range] = self.range[offset >= self.range]

            calc = (offset / self.range)
            calc[calc >= 1.0] = 1.0
            calc = calc * 65535.0
            n_array = calc.astype(np.uint16)
        else:
            return

        n_array = np.insert(n_array, self.led_insert_pos, 0)
        n_array = np.reshape(n_array, (11,22))

        img3 = cv2.resize(n_array, (int(22 * 50), int(11 * 50)), interpolation = cv2.INTER_NEAREST)
        cv2.imshow('ir', img3)
        cv2.waitKey(1)

    def detect_error(self, array):
        err_arr = []
        for i in range(len(array)):
            if array[i] == 0:
                err_arr.append(i)
        print(err_arr)

args = sys.argv

if __name__ == '__main__':
    analyzer = Analyzer()

    if len(args) == 1:
        analyzer.start()
    if len(args) == 2:
        if args[1] == 'test':
            analyzer.test()
        if args[1] == 'test2':
            analyzer.test_2()

