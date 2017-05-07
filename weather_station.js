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

// click behavior for the "Take Measurement" button
function add_new() {
    // somewhat bogus behavior: toggles between empty and provided string
    // This can probably be organized better as well. Separate spans for title and content make sense.
    status_cell = document.getElementById("status");
    testc = status_cell.innerHTML[0]
    if (testc == "W")
    	status_cell.innerHTML = "Request cancelled. Offline.";
    else if (testc == "R")
    	status_cell.innerHTML = "Offline.";
    else
    	status_cell.innerHTML = "Waiting for server response from measurement request...";
}
