'''
Testing the Pi Camera module.
Author: Michael L. Mehr
Date: May 6, 2017
Project: Weather Station v1.0
'''

from picamera import PiCamera, exc
from time import sleep
import utilities as ut

capfile = '/home/pi/Desktop/testimg.jpg'

def take_snapshot(filename, preview_delay=3, resolution=(1024,768), alpha=255, annotation=None):
    ''' Take a picture with the PyCamera module. Max.res=(2592,1944), min=(64,64)'''
    try:
        camera = PiCamera()
        camera.rotation = 90
        camera.resolution = resolution
        if annotation == None:
            annotation = "Weather Station at " + ut.make_local_timestamp()
        camera.annotate_text = annotation
        camera.start_preview(alpha=alpha)
        sleep(2 + preview_delay) # minimum 2 sec sleep for agc/autolevel lighting
        camera.capture(filename)
        camera.stop_preview()

    except exc.PiCameraMMALError:
        print """Cannot run error:
            Another process (e.g. IDLE shell) is probably using the camera.
            Please close it and try again."""

    except KeyboardInterrupt:
        camera.stop_preview()

if __name__ == "__main__":
    take_snapshot(capfile, preview_delay=0)
