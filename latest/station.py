"""
Assignment 2
Sensor Data UI Display
UCSCx Spring 2017
Michael L. Mehr, adapted from original by Gil Garcia, instructor
"""

import datetime

data_filename = "sensors.dat"
html_filename = "index.html" # index.html allows Brackets to open live link to browser
device_name = "RPi Weather Station 42X-001"

# Each sensor reading consists of triplets of 3 values, as follows:
#   Temperature - def.F, int (range TBD)
#   Pressure - inHg, float (range TBD)
#   Humidity - %, int (range TBD)
# I chose to make a list of these sensor readings.
#   The data in the list occurs in chronoligical order (earliest data first).
# It is assumed that in a real app, timestamps would probably be provided by the data gathering process,
#   but in my implementation, I add it to each reading during the data merge.
sensor_data = [
    ["80","28.33","80"],
    ["82","27.01","60"],
    ["84","29.35","40"],
]

# Some attempt has been made for flexible layout.
# I allowed the sensor column descriptions (name, tooltips) to be specified in one place for easier modification.
# This could also eventually be considered to be somewhat defined by the data gathering module as well.
column_descriptions = [ 
    {"name": "Temperature", "tip": "Units: deg.F"}, 
    {"name": "Humidity", "tip": "Units: inHg"}, 
    {"name": "Pressure", "tip": "Units: %"}, 
    {"name": "Timestamp", "tip": "Time taken (local)"}, 
]

#
# This is the main page template.
#
# I have added various features to the initial design provided by Gil Garcia:
# 1. Status line at the bottom (currently shows "comm line status" from fake AJAX transaction to load the data)
# 2. Button to take measurements (currenly just updates the status line)
# 3. Row highlighting for table rather than individual fields
# 4. Split out the data rows template for automated processing of more than one data point
# 5. Split out the column header template for easier management of sensor type columns
#
# I also tried to keep things local to the device for speed. So no use of JQuery or custom web fonts, systems, etc.
# I use the Python feature of named substitution parameters whenever possible.
# Also note the use of data subscripting in the data row template. This allows me to pass the entire reading at once.
#
template_string = '''
<html>
    <head>
        <title>IoT :: 30402 :: Assignment 2</title>
        <link rel="stylesheet" type="text/css" href="assignment2.css">
        <script src="assignment2.js"></script>
    </head>
    <body>
        <h1>Sensor Output from {sname}</h1>
        <table class="datatable">
            <tr class="dataheadrow">
                {header_columns}
            </tr>
        {data_rows}
        </table>
        <p><div class="tooltip">
        	<button class="btn info" onclick="add_new()">Take Measurement</button>
            <span class="tooltiptext">Take a new measurement (TBD)</span>
        </div></p>
        <p><div class="status"><span id="comstat">COMM STATUS: </span><span id="status">Offline.</span></div></p>
        <footer>Design: Michael L. Mehr, Gil Garcia (C) 2017</footer>
    </body>
</html>
'''

headercol_string = '''\
                <td><div class="tooltip">{name}<span class="tooltiptext">{tooltip}</span></div></td>
'''

datarow_string = '''\
            <tr class="datarow" id="datarow{num}" onmouseover="highlight('datarow{num}')" onmouseout="reset('datarow{num}')">
                <td>{data[0]}</td>
                <td>{data[1]}</td>
                <td>{data[2]}</td>
                <td>{data[3]}</td>
            </tr>
'''

def main():
    sensor_data = read_data(data_filename)
    output_html = merge_data(template_string, sensor_data, column_descriptions)
    output_data(output_html)


def merge_data(template_str, input_data, header_data):
    # Table metadata: get the names of the columns and their tooltips from a list (rather than hard-coding in the template)
    hdr_cols = ""
    for hdrcol in header_data:
        hdr_cols += headercol_string.format(name=hdrcol['name'], tooltip=hdrcol['tip'])
    # Table data: get the data rows from a dynamic list of reading triplets (each of which are lists of 3 readings as strings)
    index = 0
    table_rows = ""
    for sensor_reading in input_data:
        # Add a 'fake' timestamp to each data row (could come from the measurement hardware)
        timestamp = "{0:%a %b %d %H:%M:%S %Y}".format(datetime.datetime.now())
        datarow = sensor_reading + [timestamp]
        # Format that data reading in HTML
        table_rows += datarow_string.format(data=datarow, num=index)
        index += 1
    merge_string = template_str.format(header_columns=hdr_cols, data_rows=table_rows, sname=device_name)
    return merge_string

def output_data(str):
    output = open(html_filename,"w")
    output.write(str)
    output.close()

def read_data(fname):
    ifile = open(fname, "r")
    data = [ x.strip().split(',') for x in ifile ]
    return data


main()
