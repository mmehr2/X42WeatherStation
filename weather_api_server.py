#!/usr/bin/python3
from flask import Flask, jsonify, abort, request, make_response, url_for

import RPi.GPIO as GPIO
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT as DHT
import PCF8591 as ADC
import datetime
import sqlite3
import utilities as wsut

# init flask instance
app = Flask(__name__, static_url_path = "")

#error handlers
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad Request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not Found' } ), 404)

# Utilities
def make_json_sample(temp, press, hum, light, tstamp):
    # Convert tstamp string from unicode to regular (since maybe jsonify has issues?)
    #tstamp2 = string(tstamp)
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

# GET request handlers
@app.route('/weather/api/sensors', methods = ['GET'])
def get_sensors():
    sensor = BMP085.BMP085()
    sens_time = datetime.datetime.utcnow()
    sens_temp = sensor.read_temperature()
    sens_hum, tempx = DHT.read_retry(11, 23)
    sens_press = sensor.read_pressure()
    ADC.setup(0x48)
    sens_light = ADC.read(0)
    ts = wsut.make_db_timestamp(sens_time)
    json_data = make_json_sample(sens_temp, sens_press, sens_hum, sens_light, ts)
    print "Measurement finished at ", wsut.make_local_timestamp(datetime.datetime.now())
    return jsonify( json_data )

@app.route('/weather/api/sensors/latest', methods = ['GET'])
def get_db_sensors():
    L = 0 # light value not yet supported
    dbname = wsut.database_filename
    try:
        conn = sqlite3.connect(dbname)
        print "Opened database", dbname
        curs = conn.cursor()
        results = curs.execute("SELECT * FROM samples WHERE tstamp >= datetime('now','-5 minutes')")
        json_data = []
        # Always gets -1: print results.rowcount, " results found."
        for (T,P,H,Ts) in results:
            data = make_json_sample(T,P,H,L,Ts)
            #print "...Appending =>", data
            #json_data.append(data)
            json_data += [data]
        # print "Final JSON creation with =>", json_data
        return jsonify( { "results": json_data } )
    except:
        return jsonify({ 'error': 'Error on database extraction.' })
    finally:
        print "Closing database ", dbname
        conn.close()

# POST request hander
@app.route('/weather/api/led/<int:toggle>', methods = ['POST'])
def set_led(toggle):
    switch_status = "off"
        
    if not request.json or not "toggle" in request.json:
        abort(400)
    toggle = request.json['toggle']

    if(toggle > 0 ):
        #turn on led

        switch_status = "on"
    else:
        #turn off led

        switch_status = "off"
    return jsonify( { 'toggle': switch_status } )

# main
# Solution to 'connection refused' involves setting host to zeroes:
#  http://stackoverflow.com/questions/30554702/cant-connect-to-flask-web-service-connection-refused

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
