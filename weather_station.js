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
function api_call(route, method, body) {
    status_cell = document.getElementById("status");
    status_cell.innerHTML = "Waiting for server response from measurement request...";
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4) { 
        if (this.status == 200) {
          status_cell.innerHTML = this.responseText;
        } else {
          status_cell.innerHTML = "ERROR: " + this.status;
        }
      }
    };
    hosturl = get_api_route(route);
    xhttp.open(method, hosturl, true);
    xhttp.send(body);
}

function add_new() {
    // modified API to bypass CORS restrictions
    device_id = document.getElementById("dvcid").value;
    console.log("API:sensors DVCID:"+device_id);
    return api_call("/sensors/"+device_id, "GET", "");
}

function set_relay(onoff) {
    // modified API to bypass CORS restrictions
    device_id = document.getElementById("dvcid").value;
    if (onoff)
      action = device_id + "\1";
    else
      action = device_id + "\0";
    cmd = "/led/0/"+action
    console.log("API:"+cmd);
    return api_call(cmd, "POST", "");
}
