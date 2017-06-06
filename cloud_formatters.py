import datetime
import settings as dbs

def make_json_x42(temp, press, humid, light, utc_sample_time):
    '''Creates a JSON object as a Python dictionary from an X42WS data sample.'''
    lat = dbs.get("X42_Latitude")
    long = dbs.get("X42_Longitude")
    alt = dbs.get("X42_Altitude")
    result = {\
        "temperature": temp,
        "pressure": press,
        "humidity": humid,
        "ambient_light": light,
        "timestamp": "%sZ" % utc_sample_time.isoformat(),\
        "latitude": "%s" % lat,\
        "longitude": "%s" % long,\
        "altitude": "%s" % alt\
        }
    return result

def package(data):
    '''Takes a JSON data object as a Python dictionary. Wraps it in the proper headers.'''
    reply_url = dbs.get("Ngrok_API")
    result = {\
          "guid": "0-ZZZ123456785B",\
          "destination": "0-AAA12345678",\
          "eventTime": "%sZ" % (datetime.datetime.utcnow().isoformat()),\
          "payload": {\
             "format": "urn:com:azuresults:x42ws:sensors",\
             "reply-to": "%s" % reply_url,\
             "data": data \
           }\
        }
    return result

def package_x42(temp, press, humid, light, utc_sample_time):
    data = make_json_x42(temp, press, humid, light, utc_sample_time)
    msg = package(data)
    return msg

def package_x42list(sample):
    (temp, press, humid, light, utc_sample_time) = sample
    return package_x42(temp, press, humid, light, utc_sample_time)

    
