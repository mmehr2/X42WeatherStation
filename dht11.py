#!/usr/bin/env python
'''
Module to operate the DHT11 "humiture" module from SunFounder Sensor Kit 2.0
This measures temperature and humidity, but not as accurate as the Bosch BMP line.
Lessons refer to the Sunfounder manual.
'''
import RPi.GPIO as GPIO
import utilities as wsut


# From Sunfounder Sensor Kit 2.0 Lesson 28 (humiture which is DHT-11)
import Adafruit_DHT as DHT
DHTSensor = 11 # type, either 11 or 22
humiture_pin = 23 # pin number in BCM mode

def setup():
    ''' Init the humidity/temperature (humiture) chip DHT-11 '''
    return # no setup needed

def sample():
    ''' Return DHT-11 humidity % as float '''
    humidity, temperature = DHT.read_retry(DHTSensor, humiture_pin)
    if humidity == None: # or humidity < 20 or humidity > 80:
        humidity = 0.0
    if temperature == None:
        temperature = 0.0
    return (humidity, temperature)

def cleanup():
    return
