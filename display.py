#!/usr/bin/env python
'''
Module to operate the LCD1602 I2C module from SunFounder Sensor Kit 2.0
Lessons refer to the Sunfounder manual.
'''
import RPi.GPIO as GPIO
import utilities as wsut

import LCD1602 as LCD

# From Sunfounder Sensor Kit 2.0 Lesson 30 (LCD1602 display)
# No pin numbers needed; this is I2C

def setup():
    ''' Init and reset the LCD display '''
    LCD.init(0x27, 1)	# init(slave address, background light)
    LCD.clear()
    LCD.write(0, 0, "Weather Station")
    LCD.write(1, 1, "Setup...")

def output(line1, line2):
    ''' Format for 1602 display and send to output '''
    try:
        LCD.clear()
        LCD.write(0,0,line1)
        LCD.write(0,1,line2)
        return 0
    except IOError:
        print "IOError: most likely cause is loose 3to5v converter."
        return -1

def cleanup():
    return
