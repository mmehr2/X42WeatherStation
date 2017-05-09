See file setup.py for documentation of the hardware setup of this project.

# Operation
The 42X Weather Station is a simple environmental sensor for gathering weather-type information and uploading it to the cloud.

The X42 Weather Station provides several features for automated operation and control.
* web access from any browser
* sensors: temperature, pressure, humidity, ambient light
* camera to provide fixed view of sensor location
* relay to control external devices (currently controls 2-color LED module)
* takes sensor samples every 5 minutes (fixed timing currently)
* operation LED in bright colors turns green during sensor reading capture, pink during image capture, otherwise off
* sample readings are saved in local database on device, each timestamped in UTC
* main webpage displays latest image and last 12 hours of sample data
* RESTful API provided for programmable access and control (further documentation below)
* low- and high- resolution image capture provided in addition to regular image (API ONLY)
* relay on/off control (API ONLY)

# Weather API Documentation


curl -i -H "Content-Type: application/json" -X GET http://<rpi address>:8080/weather/api/sensors
	To report the current readings on all the sensors, returned as JSON data (one reading of all sensors exc.camera).

curl -i -H "Content-Type: application/json" -X GET http://<rpi address>:8080/weather/api/sensors/latest
	To capture all the latest current readings for the last hour on all the sensors, returned as JSON data. (typ.12 readings)

curl -i -H "Content-Type: application/json" -X GET http://<rpi address>:8080/weather/api/sensors/latest/M
	To capture all the latest current readings for the last M minutes on all the sensors, returned as JSON data.
	(Note 3)

curl -i -H "Content-Type: application/json" -X POST -d '{"action":1}' http://<rpi address>:8080/weather/api/led/0
	To turn the relay/LED on.

curl -i -H "Content-Type: application/json" -X POST -d '{"action":0}' http://<rpi address>:8080/weather/api/led/0
	To turn the relay/LED off.

curl -i -H "Content-Type: application/json" -X POST -d '{"action":1}' http://<rpi address>:8080/weather/api/camera/0
	To take a normal camera snapshot.(Note 1,2)

curl -i -H "Content-Type: application/json" -X POST -d '{"action":1}' http://<rpi address>:8080/weather/api/camera/1
	To take a low-resolution camera snapshot.(Note 1,2)

curl -i -H "Content-Type: application/json" -X POST -d '{"action":1}' http://<rpi address>:8080/weather/api/camera/2
	To take a high-resolution camera snapshot.(Note 1,2)

NOTES:
1. If action=2 is used, the image is placed in the title page of the main station web page for viewing. It will remain until the next automated sample is taken. The action=1 operation is provided to take a silent snapshot for later retrieval.

2. Optional setting "led":X provided to control use of operational LED during image capture:
X is 0, '0', or 'no': LED does not turn on during current image capture operation
X is anything else: LED operates as normal; this is the default setting.

3. M can be any integer >0 and is interpreted as the number of minutes prior to 'now' to go back to for return as JSON data.
There is no limit to the value, so the entire database could be dumped this way. There is no pagination of the data.

