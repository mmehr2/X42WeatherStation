'''
Main API server file using Flask web server
'''
from flask import Flask, jsonify, abort, request, make_response, url_for

import sys
import datetime
import sqlite3
import utilities as wsut
import sample
import pwmled as LED
import relay
import camera
from time import sleep

# Utilities
def make_json_sample(temp, press, hum, light, tstamp):
    data = [
        {
        'senstype':'temperature',
        'current':temp
        },
        {
        'senstype':'pressure',
        'current':press
        },
        {
        'senstype':'humidity',
        'current':hum
        },
        {
        'senstype':'ambient_light',
        'current':light
        }
    ]
    return { "sensors": data, "timestamp": tstamp }

def make_access_response(*args):
    ''' Follow CSOR protocol for requests from port 80  '''
    resp = make_response(*args)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

# init flask instance
app = Flask(__name__, static_url_path = "")

#error handlers
@app.errorhandler(400)
def bad_request(error):
    return make_access_response(jsonify( { 'error': 'Bad Request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_access_response(jsonify( { 'error': 'Not Found' } ), 404)

# GET request handlers
@app.route('/weather/api/sensors', methods = ['GET'])
def get_sensors():
    '''
    TEST:
    curl -i -H "Content-Type: application/json" -X GET http://12.0.0.1:8080/weather/api/sensors
    '''
    try:
        sample.open()
        X = sample.take_sample(flashLED = True)
        (sens_temp,sens_press,sens_hum,sens_light,sens_time,stlocal) = X
        ts = wsut.make_db_timestamp(sens_time)
        json_data = make_json_sample(sens_temp, sens_press, sens_hum, sens_light, ts)
        print "Measurement finished at ", wsut.make_local_timestamp(datetime.datetime.now())
        return make_access_response(jsonify( json_data ))
    except:
        e = sys.exc_info()[0]
        #print("Error on sensor sampling: %s" % e)
        return make_access_response(jsonify({ 'error': 'Error on sensor sampling: %s' % e }))
    finally:
        sample.close()

@app.route('/weather/api/sensors/latest', methods = ['GET'])
@app.route('/weather/api/sensors/latest/<int:minutes>', methods = ['GET'])
def get_db_sensors(minutes=60):
    ''' Get a subset of the data and return to the client as JSON.
    TEST:
    curl -i -H "Content-Type: application/json" -X GET http://12.0.0.1:8080/weather/api/sensors/latest
    curl -i -H "Content-Type: application/json" -X GET http://12.0.0.1:8080/weather/api/sensors/latest/15
    '''
    dbname = wsut.database_filename
    if minutes < 0:
        return jsonify( { 'error': "Unsupported query for T<0." } )
    elif minutes == 0:
        minutes = 60
    try:
        conn = sqlite3.connect(dbname)
        #print "Opened database", dbname
        curs = conn.cursor()
        recent = "-%d minutes" % minutes
        results = curs.execute("SELECT * FROM samples WHERE tstamp >= datetime('now',(?))", (recent,))
        # NOTE: results is an array of value tuples, one per row
        json_data = []
        # Always gets -1: print results.rowcount, " results found."
        for (T,P,H,L,Ts) in results:
            data = make_json_sample(T,P,H,L,Ts)
            #print "...Appending =>", data
            json_data += [data]
        # print "Final JSON creation with =>", json_data
        return make_access_response(jsonify( { 'results': json_data } ))
    except:
        e = sys.exc_info()[0]
        #print("Error on database extraction: %s" % e)
        return make_access_response(jsonify({ 'error': 'Error on database extraction: %s' % e }))
    finally:
        #print "Closing database ", dbname
        conn.close()

# POST request handers
@app.route('/weather/api/led/<int:lednum>', methods = ['POST'])
def set_led(lednum):
    '''
    TEST:
    curl -i -H "Content-Type: application/json" -X POST -d '{"action":1}' http://12.0.0.1:8080/weather/api/led/0
    '''
    if not request.json or not "action" in request.json:
        abort(400)
    action = request.json['action']
    return set_led_cmd(lednum, action)

@app.route('/weather/api/led/<int:lednum>/<int:action>', methods = ['POST'])
def set_led_cmd(lednum, action):
    if lednum != 0:
        return make_access_response(jsonify( { 'message': "Use of led not supported", 'status':-1, 'id': lednum } ))
    switch_status = "off"
    try:
        relay.setup()
        
        if action == 1 or action == '1':
            #turn on led
            relay.set(0xffffff)
            switch_status = "on"
        else:
            #turn off led
            relay.set(0)
            switch_status = "off"
        return make_access_response(jsonify( { 'message': switch_status, 'status': 0, 'id': lednum } ))
    except:
        e = sys.exc_info()[0]
        return make_access_response(jsonify( { 'message': "Could not use led: e=%s" % e, 'status':-2, 'id': lednum } ))
    finally:
        relay.cleanup()

@app.route('/weather/api/camera/<int:camnum>', methods = ['POST'])
def snap_cam(camnum):
    '''
    TEST:
    curl -i -H "Content-Type: application/json" -X POST -d '{"action":2,'led':1}' http://12.0.0.1:8080/weather/api/camera/0
    '''
    if not request.json or not "action" in request.json:
        abort(400)
    action = request.json['action']
    flash_led = True # since the LED might affect the image, we allow the user to turn it off
    if "led" in request.json:
        led_ = request.json["led"]
        if led_ == 0:
            flash_led = False
    filename = "ws_camimage.jpg"
    capfilename = filename
    if int(action) > 1:
        filename = "ws_image.jpg"
        capfilename = "/var/www/html/"+filename
    if camnum < 0 or camnum > 2:
        return make_access_response(jsonify( { 'message': "Use of camera not supported", 'status':-1, 'id': camnum } ))
    cam_status = ""
    result = 0
    try:
        if flash_led:
            LED.setup()
            LED.setColor(0xc000df)
        
        if action != 0:
            resolution = (1024,768)
            if camnum == 1:
                resolution = (2592, 1944)
            if camnum == 2:
                resolution = (100, 100)
            result = camera.take_snapshot(capfilename, preview_delay=0, alpha=0, resolution=resolution)
            if result == 0:
                (x, y) = resolution
                cam_status = "%s %ix%i" % (filename, x, y)
            elif result == -1:
                cam_status = "Cannot capture image, camera in use."
            else:  #if result == -2: or anything else for that matter
                cam_status = "Cannot capture image, camera error."
        return make_access_response(jsonify( { 'message': cam_status, 'status': result, 'id': camnum } ))
    except:
        e = sys.exc_info()[0]
        return make_access_response(jsonify( { 'message': "Could not use camera, e=%s" % e, 'status':-2, 'id': camnum } ))
    finally:
        if flash_led:
            LED.cleanup()

# main
# Solution to 'connection refused' involves setting host as well as port:
#  http://stackoverflow.com/questions/30554702/cant-connect-to-flask-web-service-connection-refused

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
