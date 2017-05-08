'''
Final Project - Weather Station
Gather Single Data Sample
UCSCx Spring 2017
Michael L. Mehr

Sample.py - take one sample for the weather station and append to file
This will be appropriate to call from cron on a regular basis (5 min for example).
Sensors:
1. Humidity via lesson 28 Humiture (DHT-11)
2. Temperature via lesson 31 Barometer (BMP-180)
3. Pressure via lesson 31 Barometer (BMP-180)
4. Ambient light via lesson 20 Photoresistor on lesson 13 PCF8591 ADC module

Outputs:
1. RGB LED from lesson 02 RGB PWM module
2. LCD 16x2 display from lesson 30 I2C LCD1602

Functionality:
1. Input data from sensors
2. Format for display on LCD1602
3. Output LED color change from data
4. Format for CSV data file
5. Append single line to data file

Data file format:
Individual data items are separated by single comma, no white space.
One data sample per line.
Order is: temperature,pressure,humid,timestamp
Units:
1. T in deg F as int
2. P in inHg as fixed point (float) w 3 digits precision
3. H in % as int 0-100 (20-80 valid by DHT-11)
<< TBD - add column for ambient light data as int from 0-255 >>
4. TIMESTAMP in ISO format if possible (YYYY-MM-DDThh:mm:ssZ) in UTC
   but for now use human-readable time in local TZ w no TZ designation
'''

import datetime
import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
import sqlite3
import sys

# Modules from this project (sensors, actuators)
import utilities as wsut
import pwmled as LED
import barometer
import display as LCD
import analog as LDR
import dht11 as DHT
import camera

init_color = 0x000000
sampling_color = 0xf0ff00
cam_color = 0xc000e0

def open():
    ''' Initialize all the hardware used for sampling.'''
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False) # only needed if my scheme for pin sharing doesn't work
    LED.setup()
    LED.setColor(init_color)
    LCD.setup()
    LDR.setup()
    barometer.setup()
    DHT.setup()

def close():
    ''' Clean up after hardware usage.'''
    DHT.cleanup()
    barometer.cleanup()
    LDR.cleanup()
    LCD.cleanup()
    LED.cleanup()
    # NEVER USE THIS FUNCTION - see WARNING in LED module for reasons.
    #GPIO.cleanup()

def outputLCD(temp, press, humid, light, htemp):
    ''' Format for 1602 display and send to output '''
    line1 = "T%1.1f P%1.3f" % (temp, press)
    line2 = "H%1.1f L%d t%1.1f" % ( humid, light, htemp)
    LCD.output(line1, line2)
    return

def formatDataCSV(temp, press, humid, local_sample_time):
    ''' Create the file format: T,P,H,Timestamp '''
    timestamp = wsut.make_local_timestamp(local_sample_time, show_seconds=True)
    line = "%d,%1.2f,%d,%s" % (temp, press, humid, timestamp)
    return line

def appendFile(fname, str):
    ''' Append data line to file '''
    output = open(fname, "a")
    output.write(str)
    output.write("\n")
    output.close()

def saveDataSQL(temp, press, humid, light, utc_sample_time):
    # Create ISO8601 timestamp YYYY-MM-DDThh:mm:ssZ in UTC
    #timestamp = "{0:%Y-%m-%dT%H:%M:%SZ}".format(utc_sample_time)
    try:
        conn = sqlite3.connect(wsut.database_filename)
        curs = conn.cursor()
        curs.execute("INSERT INTO samples values((?), (?), (?), (?), (?))",\
                     (temp, press, humid, light, utc_sample_time)  )
        conn.commit()
    except:
        e = sys.exc_info()[0]
        print("Error on database insertion: %s" % e)

def take_sample(flashLED = False):
    ''' Do the sampling, return the results.
    Returns a tuple of (T, P, H, L, tmu, tm) where:
        T = temperature in degrees F as float
        P = pressure in inHg (inches of mercury) as float
        H = humidity in % as int
        L = ambient light (no units) as byte from 0-255
        tmu = sampling time as datetime object in UTC
        tm = sampling time similar but in local time
    '''
    if flashLED:
        LED.setColor(sampling_color)
    samptime = datetime.datetime.now()
    samptime_utc = datetime.datetime.utcnow()
    L = LDR.sample()
    (T, P) = barometer.sample()
    (H, Tx) = DHT.sample() # may take seconds!
    outputLCD(T, P, H, L, Tx)
    if flashLED:
        LED.setColor(init_color)
    return (T, P, H, L, samptime_utc, samptime)

def run():
    open()
    X  = take_sample(flashLED = True)
    #print X
    (T, P, H, L, samptime_utc, tmlocal) = X
    print T, P, H, L
    print samptime_utc
    saveDataSQL(T, P, H, L, samptime_utc)
    LED.setColor(cam_color)
    camera.take_snapshot(wsut.image_filename, preview_delay=0, alpha=0)
    LED.setColor(init_color)
    close()

if __name__ == "__main__":
    run()
    
