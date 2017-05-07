See file setup.py for documentation of the hardware setup of this project.

How to trigger the POST commands for the weather API:
curl -i -H "Content-Type: application/json" -X POST -d '{"toggle":1}' http://192.168.1.154:8080/weather/api/led/0
	To turn the LED on.

curl -i -H "Content-Type: application/json" -X POST -d '{"toggle":0}' http://192.168.1.154:8080/weather/api/led/0
	To turn the LED off.

curl -i -H "Content-Type: application/json" -X POST -d '{"action":1}' http://192.168.1.154:8080/weather/api/camera/0
	To take a normal camera snapshot.

curl -i -H "Content-Type: application/json" -X POST -d '{"action":1}' http://192.168.1.154:8080/weather/api/camera/1
	To take a low-resolution camera snapshot.

curl -i -H "Content-Type: application/json" -X POST -d '{"action":1}' http://192.168.1.154:8080/weather/api/camera/2
	To take a high-resolution camera snapshot.
