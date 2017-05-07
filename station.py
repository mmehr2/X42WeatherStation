"""
Final Project - Weather Station
Sensor Data UI Display (create HTML file)
UCSCx Spring 2017
Michael L. Mehr, adapted from original by Gil Garcia, instructor
"""

import datetime
import utilities as wsut
import sqlite3

# Each sensor reading consists of triplets of 3 values, as follows:
#   Temperature - def.F, int (range TBD)
#   Pressure - inHg, float w.2 decimals (range TBD)
#   Humidity - %, int (range 0-100)
# I chose to make a list of these sensor readings.
#   The data in the list occurs in chronoligical order (earliest data first).
# This is only default data; it will be overwritten by file import.
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
    {"name": "Pressure", "tip": "Units: inHg"}, 
    {"name": "Humidity", "tip": "Units: %"}, 
    {"name": "Light", "tip": "Units: 0-255"}, 
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
        <title>{sname}</title>
        <link rel="stylesheet" type="text/css" href="{project}.css">
        <script src="{project}.js"></script>
    </head>
    <body>
        <h1>Sensor Output from {sname}</h1>
        <p class="notes">NOTE: Scroll down for data below image.</p>
        <div class="imgdiv">
            <img src="ws_image.jpg" alt="Image Snapshot by Weather Station Camera" >
        </div>
        <p><table class="datatable">
            <tr class="dataheadrow">
                {header_columns}
            </tr>
        {data_rows}
        </table></p>
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
                <td>{data[4]}</td>
            </tr>
'''

def merge_data(template_str, input_data, header_data):
    # Table metadata: get the names of the columns and their tooltips from a list (rather than hard-coding in the template)
    hdr_cols = ""
    for hdrcol in header_data:
        hdr_cols += headercol_string.format(name=hdrcol['name'], tooltip=hdrcol['tip'])
    # Table data: get the data rows from a dynamic list of reading triplets (each of which are lists of 3 readings as strings)
    index = 0
    table_rows = ""
    for sensor_reading in input_data:
        # Format that data reading in HTML
        table_rows += datarow_string.format(data=sensor_reading, num=index)
        index += 1
    merge_string = template_str.format(header_columns=hdr_cols, data_rows=table_rows, sname=wsut.device_name, project=wsut.project_name)
    return merge_string

def output_data(fname, str):
    output = open(fname,"w")
    output.write(str)
    output.close()

def read_data(fname):
    ifile = open(fname, "r")
    data = [ x.strip().split(',') for x in ifile ]
    return data

def read_dbdata(dbname):
    #dbname = wsut.database_filename
    try:
        conn = sqlite3.connect(dbname)
        #print "Opened database", dbname
        curs = conn.cursor()
        results = curs.execute("SELECT * FROM samples WHERE tstamp >= datetime('now','-12 hours')")
        output_data = [[T,P,H,L,Ts] for (T,P,H,L,Ts) in results]
        #for (T,P,H,L,Ts) in results:
        #    data = [T,P,H,L,Ts]
        #    #print "...Appending =>", data
        #    output_data += [data]
        # print "Final JSON creation with =>", json_data
        return output_data
    except:
        print 'Error on database extraction.'
        return []
    finally:
        #print "Closing database ", dbname
        conn.close()

def main():
    #sensor_data = read_data(wsut.data_filename)
    sensor_data = read_dbdata(wsut.database_filename)
    #print sensor_data
    output_html = merge_data(template_string, sensor_data, column_descriptions)
    output_data(wsut.html_filename, output_html)

if __name__ == "__main__":
    main()
