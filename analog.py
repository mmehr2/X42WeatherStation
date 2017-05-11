#!/usr/bin/env python
'''
Module to operate the photoresistor module from SunFounder Sensor Kit 2.0
Lessons refer to the Sunfounder manual.
'''
import RPi.GPIO as GPIO
import utilities as wsut

import PCF8591 as ADC

# From Sunfounder Sensor Kit 2.0 Lesson 20 (photoresistor)
# NOTE: The PFC8591 has four analog inputs 0-3. we only use 1 for now.

A0 = 0
A1 = 1
A2 = 2
A3 = 3

min_voltage = 0
max_voltage = 255

ldr_pin = A0

def setup():
    ''' Initialization for LDR hardware input '''
    ADC.setup(0x48)

def sample(pin = ldr_pin):
    ''' Return voltage as int 0-255 '''
    sample = ADC.read(pin)
    return sample

def convertLDR(voltage):
    ''' Returns a number that increases for increasing light levels. '''
    return max_voltage - voltage

def readLDR():
    ss = sample(ldr_pin)
    value = convertLDR(ss)
    return value

def cleanup():
    return
