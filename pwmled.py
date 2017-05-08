#!/usr/bin/env python
'''
Module to operate PWM LED from SunFounder Sensor Kit 2.0
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

# From Lesson 02 (RGB LED with PWM)
# NOTE: Pin numbers have been modified for BCM mode
# NOTE: Pin numbers have further been modified for my circuit
R = 17
G = 18
B = 27 # for later model Pi's only, else 21
# See discussion here: https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering

def setup(Rpin=R, Gpin=G, Bpin=B):
    global ledpins
    global p_R, p_G, p_B
    if GPIO.getmode() != GPIO.BCM:
        GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)
    ledpins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    GPIO.setup(ledpins.values(), GPIO.OUT, initial=GPIO.HIGH)    # Turn off all leds
    
    # set Frequecy to 2KHz (5kHz blue)
    p_R = GPIO.PWM(ledpins['pin_R'], 2000)
    p_G = GPIO.PWM(ledpins['pin_G'], 1999)
    p_B = GPIO.PWM(ledpins['pin_B'], 5000)
    
    # Initial duty Cycle = 0(leds off)
    p_R.start(100)
    p_G.start(100)
    p_B.start(100)

def map(x, in_min, in_max, out_min, out_max):
    ''' Map a value from its range (in_min, in_max) to another range (out_min, out_max).'''
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def off():
    GPIO.setup(ledpins.values(), GPIO.IN)    # Turn off all leds

def setColor(col):   # For example : col = 0x112233
    ''' Send hex color to LED '''
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0
    
    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)
    
    p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
    p_G.ChangeDutyCycle(100-G_val)
    p_B.ChangeDutyCycle(100-B_val)

def setRGB(colorR, colorG, colorB):
    col = wsut.makeColor(colorR, colorG, colorB)
    setColor(col)
    return

def cleanup():
    ''' Clean up after LED usage. '''
    p_R.stop()
    p_G.stop()
    p_B.stop()
    off()

