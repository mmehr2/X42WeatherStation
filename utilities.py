'''
Utility functions.
Author: Michael L. Mehr
Date: May 6, 2017
Project: Weather Station v1.0
'''
import datetime

device_name = "RPi Weather Station X42-v1"
project_name = "weather_station"
image_filename = "ws_image.jpg"
data_filename = "sensors.dat"
html_filename = "index.html"
database_filename = 'weather_station.db'
data_topic_name = 'x42ws.public.data'
command_topic_name = 'x42ws.public.commands'

# Website color scheme inspired by a web article
'''
    Color scheme inspiration from: #24 from https://designschool.canva.com/blog/website-color-schemes/
    Color elements: Deep purple (6E3667), Electric lime (88D317), White (fff), and Light Blue (4da6ff)
'''
web_color_background = 0x6E3667 # deep purple
web_color_foreground = 0xffffff # white
web_color_hilight1 = 0x88D317 # electric lime
web_color_hilight2 = 0x4da6ff # light blue
# Same, tweaked for PWMLED module
pwm_color_background = 0xc000e0 # deep purple / magenta
pwm_color_foreground = 0xffffff # white
pwm_color_hilight1 = 0xf0ff00 # electric lime
pwm_color_hilight2 = 0x2d86ff # light blue

def make_db_timestamp(utc_sample_time=datetime.datetime.utcnow()):
    ''' Create ISO8601 timestamp YYYY-MM-DDThh:mm:ssZ in UTC '''
    timestamp = "{0:%Y-%m-%dT%H:%M:%SZ}".format(utc_sample_time)
    return timestamp

def make_local_timestamp(local_time=datetime.datetime.now(), show_seconds=False):
    ''' Create Iocaltimestamp e.g."Wed Mar 22 2017 04:23:00" in local timezone '''
    if show_seconds:
        formatter = "{0:%a %b %d %Y %H:%M:%S}"
    else:
        formatter = "{0:%a %b %d %Y %H:%M}"
    timestamp = formatter.format(local_time)
    return timestamp

def makeColor(red, green, blue):
    ''' Create a 24-bit color from 8-bit RGB values '''
    col = ( ((red & 0xFF) << 16) | ((green & 0xFF) << 8) | ((blue & 0xFF) << 0) )
    return col
