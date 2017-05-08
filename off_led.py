#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

pin_list = [17, 18, 27]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_list, GPIO.IN)
