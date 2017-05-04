#!/usr/bin/python3
from flask import Flask, jsonify, abort, request, make_response, url_for

import RPi.GPIO as GPIO
import Adafruit_BMP.BMP085 as BMP085
#from Adafruit_GPIO.GPIO import *

# init flask instance
app = Flask(__name__, static_url_path = "")

#error handlers
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad Request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not Found' } ), 404)

# GET request handler
@app.route('/assignment7/api/sensors', methods = ['GET'])
def get_sensors():
    sensor = BMP085.BMP085()
    sens_temp = sensor.read_temperature()
    sens_hum = 80
    sens_press = sensor.read_pressure()
    json_data = {
        'senstype':'temperature',
        'current':sens_temp
    }
    return jsonify( { 'sensors': json_data } )

# POST request hander
@app.route('/assignment7/api/led/<int:toggle>', methods = ['POST'])
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
if __name__ == '__main__':
    app.run(debug=True, port=8080)
