/*  assignment 2
    javascript support library
    UCSCx Spring 2017
    Gil Garcia, mods by Michael L. Mehr
*/

// mouseover behavior to highlight table row cells
function highlight(tag) {
    sensor_cell = document.getElementById(tag);
    sensor_cell.style.fontWeight="bold";
    sensor_cell.style.fontSize="120%";
    sensor_cell.style.color="#ffffff";
}

// mouseover behavior to UN-highlight table row cells
function reset(tag) {
    sensor_cell = document.getElementById(tag);
    sensor_cell.style.fontWeight="normal";
    sensor_cell.style.color="#88D317";
    sensor_cell.style.fontSize="100%";
}

// create cross-site route to weather-station RESTful API
function get_api_route(route) {
    hosturl_ = self.location.hostname
    if (hosturl_ == "")
        hosturl_ = "localhost";
    hosturl = "http://" + hosturl_ +  ":8080/weather/api" + route;
    console.log(hosturl);
    return hosturl;
}

// click behavior for the "Take Measurement" button
function api_call(route, method, body, callbackfunc=null) {
    status_cell = document.getElementById("status");
    status_cell.innerHTML = "Waiting for server response from measurement request...";
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4) { 
        if (this.status == 200) {
          status_cell.innerHTML = this.responseText;
        } else {
          status_cell.innerHTML = "ERROR:" + this.status + " (" + this.statusText + ")";
        }
        if (typeof(callbackfunc) == "function") {
          callbackfunc(this); // pass the xhttp object
        }
      }
    };
    hosturl = get_api_route(route);
    xhttp.open(method, hosturl, true);
    if (body == "")
      xhttp.send();
    else
      xhttp.send(body);
}

function fround(num, places) {
  for (var i=0, j=1.0; i<places; ++i) {
    j *= 10.0;
  }
  return Math.round(num * j)/j;
}

function add_new() {
    status_cell = document.getElementById("status");
    callback = function(xo) {
	if (xo.status != 200) return;
	json = JSON.parse(xo.responseText)
	data = json.sensors;
	timestamp = json.timestamp;
	result = "Data @ " + timestamp + ":<br/>"
	result += "<ul>";
	for (var i in data) {
	  type_name = data[i].senstype;
	  type_val = data[i].current;
	  if (type_name == "temperature")
	    type_val = fround(type_val, 1);
	  if (type_name == "pressure")
	    type_val = fround(type_val, 2);
	  if (type_name == "humidity")
	    type_val = fround(type_val, 1);
	  result += "<li>" + type_name + "=" + type_val + "</li>"
	}
	result += "</ul>";
	status_cell.innerHTML = result;
    }
    return api_call("/sensors", "GET", "", callback);
}

function set_relay() {
    relay_btn = document.getElementById("rlybtn"); // Device ON/OFF
    relay_tip = document.getElementById("rlytip"); // Turn device ON/OFF
    state = relay_btn.innerHTML[8];
    onoff = (state == 'N');
    console.log("Inner[]=",state,",ON=",onoff);
    if (onoff) {
      action = "/led/0/1";
    } else {
      action = "/led/0/0";
    }
    callback = function(xo) {
	if (xo.status != 200) return;
	console.log("From callback: ON=", onoff);
	if (onoff) {
	  relay_btn.innerHTML = "Device OFF";
	  relay_tip.innerHTML = "Turn device OFF";
	} else {
	  relay_btn.innerHTML = "Device ON";
	  relay_tip.innerHTML = "Turn device ON";
	}
    }
    return api_call(action, "POST", "", callback);
}

function cam_pic(type) {
    action = "/camera/"+String(type)+"/3"; // med.res, flash, www pic
    callback = function(xo) {
	if (xo.status != 200) return;
	console.log("Reloading page");
	window.location.reload();
    }
    return api_call(action, "POST", "", callback);
}
