#!/usr/bin/python

"""
Gil Garcia
UCSC IoT 30402
Spring 2017
Assignment #5 - Controlling Devices Using CGI
"""

import time, sys
import cgi, cgitb
import RPi.GPIO as GPIO

cgitb.enable()

GPIO.setmode(GPIO.BCM)

red_pin = 17
green_pin = 18
blue_pin = 27

rgb_color = [0,0,0]

freq = 100

duration = 1

GPIO.setup(red_pin,GPIO.OUT)
GPIO.setup(green_pin,GPIO.OUT)
GPIO.setup(blue_pin,GPIO.OUT)

RED = GPIO.PWM(red_pin, freq)
GREEN = GPIO.PWM(green_pin, freq)
BLUE = GPIO.PWM(blue_pin, freq)

RED.start(0)
GREEN.start(0)
BLUE.start(0)

def color(R, G, B, duration):
    RED.ChangeDutyCycle(R)
    GREEN.ChangeDutyCycle(G)
    BLUE.ChangeDutyCycle(B)
    time.sleep(duration)

def run(hex_color):
    rgb_color[0] = int(hex_color[0:2],16)  #red
    rgb_color[1] = int(hex_color[2:4],16)  #green
    rgb_color[2] = int(hex_color[4:6],16)  #blue

    percent_red = 100-(rgb_color[0]/255*100)
    percent_green = 100-(rgb_color[1]/255*100)
    percent_blue = 100-(rgb_color[2]/255*100)

    color(percent_red, percent_green, percent_blue, duration)

def destroy():
    RED.stop()
    GREEN.stop()
    BLUE.stop()

    GPIO.output(red_pin, GPIO.HIGH)
    GPIO.output(green_pin, GPIO.HIGH)
    GPIO.output(blue_pin, GPIO.HIGH)
    GPIO.cleanup()

def main():
    form=cgi.FieldStorage()
    
    html="""<html><head><title>Assignment 5 :: CGI Color</title></head><body>
    <h1>Assignment 5 - CGI Colors</h1>
    <p>Enter a hex color code (Ex: 00FF00):
        <form method="post" action="/cgi-bin/assignment5.py"> 
            <input type="text" name="textcolor" />
            <input type="submit" value="Change Hex Color Code" />
        </form>
    </p>    
    """
    print("Content-type: text/html\n\n")    
    print(html)
    
    if "textcolor" in form:
        hex_color = form["textcolor"].value
        hex_color = hex_color.upper()
        hex_color = hex_color.lstrip('#')
        hex_color = cgi.escape(hex_color)
        
        response_text = """<p>You set the color to: <span style="color:{0};">{0}</span></p>"""

        update_text = response_text.format(hex_color)

        print(update_text)

        run(hex_color)
        destroy()
    
    print("""</body></html>""")


main()
