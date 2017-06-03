import datetime

def make_json_x42(temp, press, humid, light, utc_sample_time):
    '''Creates a JSON object as a Python dictionary from an X42WS data sample.'''
    result = {\
        "temperature": temp,
        "pressure": press,
        "humidity": humid,
        "ambient_light": light,
        "timestamp": "%sZ" % utc_sample_time.isoformat()\
        }
    return result

def package(data):
    '''Takes a JSON data object as a Python dictionary. Wraps it in the proper headers.'''
    result = {\
          "guid": "0-ZZZ123456785B",\
          "destination": "0-AAA12345678",\
          "eventTime": "%sZ" % (datetime.datetime.utcnow().isoformat()),\
          "payload": {\
             "format": "urn:com:azuresults:x42ws:sensors",\
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

    
