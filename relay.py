#!/usr/bin/env python
'''
Module to operate the relay module from SunFounder Sensor Kit 2.0
Lessons refer to the Sunfounder manual.

# WARNING: use of GPIO.cleanup() will shut off all output pins!
Basically, it sets every channel to IN mode, which plays havoc with any outputs.
Trying to get a web server to control an output persistently means NEVER calling
that function!
This module is designed to work with other persistent outputs.
Instead of calling GPIO.cleanup(), it sets all pins it uses to IN mode.
'''
import RPi.GPIO as GPIO
import utilities as wsut

# From Sunfounder Sensor Kit 2.0 Lesson 04 (relay)
# NOTE: This will drive the 2-color LED, on=green, off=red
RelayPin = 24

def setup():
    if GPIO.getmode() != GPIO.BCM:
        GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)
    GPIO.setup(RelayPin, GPIO.OUT, initial=GPIO.LOW)

def set(on):
    if on != 0:
        GPIO.output(RelayPin, GPIO.HIGH)
    else:
        GPIO.output(RelayPin, GPIO.LOW)

def cleanup():
    GPIO.setup(RelayPin, GPIO.IN)
