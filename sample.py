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
GPIO.setmode(GPIO.BCM)

# From Lesson 20 (photoresistor)
import PCF8591 as ADC
adc_pin = 17

# From Lesson 28 (humiture which is DHT-11)
import Adafruit_DHT as DHT
DHTSensor = 11 # type, either 11 or 22
humiture_pin = 23 # pin number in BCM mode

# From Lesson 30 (LCD1602 display)
import LCD1602 as LCD

# From Lesson 31 (barometer)
import Adafruit_BMP.BMP085 as BMP085
# No pin numbers needed; this is I2C

data_filename = "sensors.dat"

def setupLDR():
    ''' Initialization for LDR hardware input '''
    ADC.setup(0x48)
    GPIO.setup(adc_pin, GPIO.IN)

def setupBarometer():
    ''' Init the barometer chip BMP-180 '''
    global barometer
    barometer = BMP085.BMP085()

def setupHumiture():
    ''' Init the humidity/temperature (humiture) chip DHT-11 '''
    return # no setup needed

def setupLCD():
    ''' Init and reset the LCD display '''
    LCD.init(0x27, 1)	# init(slave address, background light)
    LCD.clear()
    LCD.write(0, 0, "Weather Station")
    LCD.write(1, 1, "Setup...")

def initialize():
    ''' Initialize all the hardware used '''
    setupLCD()
    setupLDR()
    setupBarometer()
    setupHumiture()

def sampleBarometer():
    ''' Return BMP-180 temp *F and press inHg as float tuple (T,P) '''
    temp = barometer.read_temperature()
    # convert deg.C to deg.F
    temp = temp * 1.80 + 32.0
    press = barometer.read_pressure()
    # convert pascals to inHg
    press = press / 3386.38866667
    return (temp, press)

def sampleHumiture():
    ''' Return DHT-11 humidity % as float '''
    humidity, temperature = DHT.read_retry(DHTSensor, humiture_pin)
    if humidity == None: # or humidity < 20 or humidity > 80:
        humidity = 0.0
    if temperature == None:
        temperature = 0.0
    return (humidity, temperature)

def sampleAmbient():
    ''' Return photoresistor voltage as int 0-255 '''
    sample = ADC.read(0)
    return sample

def convertToColor(temp, press, humid, light):
    ''' Make LED colors as some function of sensor data '''
    red = 100
    green = 20
    blue = 75
    return (red, green, blue)

def outputLED(colorR, colorG, colorB):
    return

def outputLCD(temp, press, humid, light, htemp):
    ''' Format for 1602 display and send to output '''
    line1 = "T%1.1f P%1.3f" % (temp, press)
    line2 = "H%1.1f L%d t%1.1f" % ( humid, light, htemp)
    LCD.clear()
    LCD.write(0,0,line1)
    LCD.write(0,1,line2)
    return

def formatDataCSV(temp, press, humid):
    ''' Create the file format: T,P,H,Timestamp '''
    timestamp = "{0:%a %b %d %H:%M:%S %Y}".format(datetime.datetime.now())
    line = "%d,%1.2f,%d,%s" % (temp, press, humid, timestamp)
    return line

def appendFile(fname, str):
    ''' Append data line to file '''
    output = open(fname, "a")
    output.write(str)
    output.write("\n")
    output.close()

def do_sample():
    (T, P) = sampleBarometer()
    (H, Tx) = sampleHumiture()
    L = sampleAmbient()
    data = formatDataCSV(T, P, H)
    appendFile(data_filename, data)
    outputLCD(T, P, H, L, Tx)
    (red, green, blue) = convertToColor(T, P, H, L)
    outputLED(red, green, blue)

def main():
    initialize()
    do_sample()

main()
    
