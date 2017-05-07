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

import utilities as wsut
import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import sqlite3
database_filename = 'weather_station.db'
import camera

# From Lesson 02 (RGB LED with PWM)
# NOTE: Pin numbers have been modified for BCM mode
R = 17
G = 18
B = 27 # for later model Pi's only, else 21
# See discussion here: https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering
init_color = 0xf0ff00

# From Lesson 20 (photoresistor)
import PCF8591 as ADC

# From Lesson 28 (humiture which is DHT-11)
import Adafruit_DHT as DHT
DHTSensor = 11 # type, either 11 or 22
humiture_pin = 23 # pin number in BCM mode

# From Lesson 30 (LCD1602 display)
import LCD1602 as LCD
# No pin numbers needed; this is I2C

# From Lesson 31 (barometer)
import Adafruit_BMP.BMP085 as BMP
# No pin numbers needed; this is I2C

def setupLDR():
    ''' Initialization for LDR hardware input '''
    ADC.setup(0x48)

def setupBarometer():
    ''' Init the barometer chip BMP-180 '''
    global barometer
    barometer = BMP.BMP085()

def setupHumiture():
    ''' Init the humidity/temperature (humiture) chip DHT-11 '''
    return # no setup needed

def setupLCD():
    ''' Init and reset the LCD display '''
    LCD.init(0x27, 1)	# init(slave address, background light)
    LCD.clear()
    LCD.write(0, 0, "Weather Station")
    LCD.write(1, 1, "Setup...")

def setupLED(Rpin, Gpin, Bpin):
    global ledpins
    global p_R, p_G, p_B
    ledpins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    for i in ledpins:
        GPIO.setup(ledpins[i], GPIO.OUT)   # Set pins' mode is output
        GPIO.output(ledpins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
    
    # set Frequecy to 2KHz (5kHz blue)
    p_R = GPIO.PWM(ledpins['pin_R'], 2000)
    p_G = GPIO.PWM(ledpins['pin_G'], 2000)
    p_B = GPIO.PWM(ledpins['pin_B'], 2000)
    
    # Initial duty Cycle = 0(leds off)
    p_R.start(100)
    p_G.start(100)
    p_B.start(100)

def map(x, in_min, in_max, out_min, out_max):
    ''' Map a value from an input rage (in_min, in_max) to an output range (out_min, out_max).'''
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def offLED():
    for i in ledpins:
        GPIO.output(ledpins[i], GPIO.HIGH)    # Turn off all leds

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

def initialize():
    ''' Initialize all the hardware used '''
    setupLCD()
    setupLED(R, G, B)
    setColor(init_color)
    setupLDR()
    setupBarometer()
    setupHumiture()

def destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    offLED()
    GPIO.cleanup()

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

def outputLED(colorR, colorG, colorB):
    col = wsut.makeColor(colorR, colorG, colorB)
    setColor(col)
    return

def outputLCD(temp, press, humid, light, htemp):
    ''' Format for 1602 display and send to output '''
    line1 = "T%1.1f P%1.3f" % (temp, press)
    line2 = "H%1.1f L%d t%1.1f" % ( humid, light, htemp)
    try:
        LCD.clear()
        LCD.write(0,0,line1)
        LCD.write(0,1,line2)
    except IOError:
        print "IOError: most likely cause is loose 3to5v converter."
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

def saveDataSQL(temp, press, humid, utc_sample_time):
    # Create ISO8601 timestamp YYYY-MM-DDThh:mm:ssZ in UTC
    #timestamp = "{0:%Y-%m-%dT%H:%M:%SZ}".format(utc_sample_time)
    try:
        conn = sqlite3.connect(database_filename)
        curs = conn.cursor()
        curs.execute("INSERT INTO samples values((?), (?), (?), (?))",\
                     (temp, press, humid, utc_sample_time)  )
        conn.commit()
    except:
        print("Error on database insertion.")

def do_sample():
    samptime = datetime.datetime.now()
    samptime_utc = datetime.datetime.utcnow()
    L = sampleAmbient()
    (T, P) = sampleBarometer()
    (H, Tx) = sampleHumiture() # may take seconds!
    data = formatDataCSV(T, P, H, samptime)
    appendFile(wsut.data_filename, data)
    saveDataSQL(T, P, H, samptime_utc)
    outputLCD(T, P, H, L, Tx)

def take_sample():
    initialize()
    do_sample()
    outputLED(0xc0, 0x00, 0xe0)
    camera.take_snapshot(wsut.image_filename, preview_delay=0, alpha=0)
    destroy()


if __name__ == "__main__":
    take_sample()
    
