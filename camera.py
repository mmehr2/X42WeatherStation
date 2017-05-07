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
    ''' Take a picture with the PyCamera module. Max.res=(2592,1944), min=(64+,64+)'''
    if annotation == None:
        annotation = "Weather Station at " + ut.make_local_timestamp()
    # Calcs to scale the annotation text size to rougly match the resolution
    (W,H) = resolution
    (Wmax,Hmax) = (2592,1944)
    (Wmin,Hmin) = (100, 100) # 64x64 does NOT work
    if W < Wmin or W > Wmax:
        print "Resolution not supported: W=", W
        return -3
    if H < Hmin or H > Hmax:
        print "Resolution not supported: H=", H
        return -4
    hscale = float(W - Wmin) / float(Wmax - Wmin)
    (ATSmin, ATSmax) = (10, 80) # actual range is 6-160, but we don't want it taking up the whole screen!
    atsize = ATSmin + hscale * (ATSmax - ATSmin)
    atsize = int(round(atsize))
    #print "AT size =", atsize, "Resolution=", (W,H), "hscale=", hscale, "range=", (ATSmin,ATSmax)
    try:
        camera = PiCamera()
        camera.rotation = 90
        camera.resolution = resolution
        camera.annotate_text = annotation
        camera.annotate_text_size = atsize
        camera.start_preview(alpha=alpha)
        sleep(2 + preview_delay) # minimum 2 sec sleep for agc/autolevel lighting
        camera.capture(filename)
        return 0
    except exc.PiCameraMMALError:
        print """Cannot run error:
            Another process (e.g. IDLE shell) is probably using the camera.
            Please close it and try again."""
        return -1
    except ValueError:
        print "Camera value error occurred."
        return -5
    except:
        print "Other camera error occurred."
        return -2
    finally:
        camera.stop_preview()
        camera.close()

if __name__ == "__main__":
    take_snapshot(capfile, preview_delay=0)
