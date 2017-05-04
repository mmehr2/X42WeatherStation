#!/usr/bin/python3

"""
Gil Garcia
UCSC IoT 30402
Spring 2017
Assignment #4 - Command-Line Controlling Devices

This program displays 1 color based on the hexadecimal color scale for RGB.  

This program runs from the command-line.  It requires a 6-digit hexadecimal
color code as an command-line argument. This code also assumed that you are using the sunfounder PWM-based
RGB (3-color) module wired to the GPIO pins specified below in the code 

Sample color codes: 
red = ff0000
purple = 990099 
black=000000
orange = ff6600

Command-line examples:
python3 assignment4.py ff0000
python3 assignment4.py 990099
python3 assignment4.py ff6600

use www.w3schools.com/colors/color_picker.asp to choose your color
"""


import time, sys
import RPi.GPIO as GPIO

cmdargs = []

# set bus mode to broadcom
GPIO.setmode(GPIO.BCM)

# assign GPIO pins to color "leads"
red_pin = 17
green_pin = 18
blue_pin = 27

# RGB colors
rgb_color = [0,0,0] # init colors

# assign off value to PWM freqency (in Hz)
freq = 100

# assign duration time in Seconds 
duration = 1

# config pins as output
GPIO.setup(red_pin,GPIO.OUT)
GPIO.setup(green_pin,GPIO.OUT)
GPIO.setup(blue_pin,GPIO.OUT)

#init pins as PWM objects and off
RED = GPIO.PWM(red_pin, freq)
GREEN = GPIO.PWM(green_pin, freq)
BLUE = GPIO.PWM(blue_pin, freq)

# init PWM pin's duty cycle to 0 (off)
RED.start(0)
GREEN.start(0)
BLUE.start(0)

#color function
def color(R, G, B, duration):
    # Color brightness range is 0-100%
    RED.ChangeDutyCycle(R)
    GREEN.ChangeDutyCycle(G)
    BLUE.ChangeDutyCycle(B)
    time.sleep(duration)
 
    # Turn all LEDs off after on_time seconds
    RED.ChangeDutyCycle(0)
    GREEN.ChangeDutyCycle(0)
    BLUE.ChangeDutyCycle(0)

# run!
def run(hex_color):
    # convert into decimal whole number
    rgb_color[0] = int(hex_color[0:2],16)  #red
    rgb_color[1] = int(hex_color[2:4],16)  #green
    rgb_color[2] = int(hex_color[4:6],16)  #blue

    # calculate percentage duration
    # colors are determined by percentage of time for PWM
    percent_red = 100-(rgb_color[0]/255*100)
    percent_green = 100-(rgb_color[1]/255*100)
    percent_blue = 100-(rgb_color[2]/255*100)

    # run color
    color(percent_red, percent_green, percent_blue, duration)

def destroy():
    RED.stop()
    GREEN.stop()
    BLUE.stop()
    GPIO.output(red_pin, GPIO.HIGH)    # Turn off all leds
    GPIO.output(green_pin, GPIO.HIGH)
    GPIO.output(blue_pin, GPIO.HIGH)
    GPIO.cleanup()
	
def main(arg):
    cmdarg = arg
    try:
        hex_color = cmdarg
        hex_color = hex_color.upper()

        if len(hex_color) == 6:
            print("running...")
            run(hex_color)
            destroy()
        else:
            print("Error: need 6 hexadecimal digits!")
            print("quitting...")
            destroy()
            quit()
    except KeyboardInterrupt:
        destroy()
  

main(sys.argv[1])
