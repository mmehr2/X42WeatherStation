#!/usr/bin/env python
'''
Module to operate the barometer module from SunFounder Sensor Kit 2.0
Lessons refer to the Sunfounder manual.
'''
import RPi.GPIO as GPIO
import utilities as wsut


# From Lesson 31 (barometer)
import Adafruit_BMP.BMP085 as BMP
# No pin numbers needed; this is I2C

def setup():
    ''' Init the barometer chip BMP-180 '''
    global barometer
    barometer = BMP.BMP085()

def sample():
    ''' Return BMP-180 temp *F and press inHg as float tuple (T,P) '''
    temp = barometer.read_temperature()
    # convert deg.C to deg.F
    temp = temp * 1.80 + 32.0
    press = barometer.read_pressure()
    # convert pascals to inHg
    press = press / 3386.38866667
    return (temp, press)

def cleanup():
    return
