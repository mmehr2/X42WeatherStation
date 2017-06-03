'''
Send a batch of data samples to the Cloud (via Kafka Producer).
Author: Michael L. Mehr
Date: June 2, 2017
Project: Weather Station v1.0
'''

import sys
import datetime
import sqlite3
import utilities as wsut
import settings as dbs
import ws_cloud_sender as cloud
import cloud_formatters as cfmt
import json

def read_sample_count():
    dbname = wsut.database_filename
    output_data = []
    try:
        conn = sqlite3.connect(dbname)
        #print "Opened database", dbname
        curs = conn.cursor()
        results = curs.execute("SELECT COUNT(*) FROM samples")
        output_data = curs.fetchone()[0]
        #print "Final JSON creation with =>", output_data
    except:
        e = sys.exc_info()[0]
        #print 'Error on database extraction: %s' % e
    #print "Closing database ", dbname
    conn.close()
    return output_data

def convTime(tstr):
    return datetime.datetime.strptime(tstr, "%Y-%m-%d %H:%M:%S.%f")

def read_samples(startRowid, endRowid):
    dbname = wsut.database_filename
    output_data = []
    try:
        conn = sqlite3.connect(dbname)
        #print "Opened database", dbname
        curs = conn.cursor()
        results = curs.execute("SELECT * FROM samples WHERE rowid >= (?) AND rowid <= (?)", (startRowid, endRowid))
        output_data = [[float(T),float(P),float(H),float(L),convTime(Ts)] for (T,P,H,L,Ts) in results]
        #print "Final JSON creation with =>", output_data
    except:
        e = sys.exc_info()[0]
        #print 'Error on database extraction: %s' % e
    #print "Closing database ", dbname
    conn.close()
    return output_data

def get_json_samples(startRowid, endRowid):
    results = read_samples(startRowid, endRowid)
    #for (index, result) in enumerate(results):
    #    T,P,H,L,tm = result
    #    print index, ": T", T, "P", P, "H", H, "L", L , "tm", tm.isoformat()
    results = [cfmt.package_x42list(x) for x in results]
    #print "Results:", results
    return results

if __name__=='__main__':
    argc = len(sys.argv)
    if argc < 3:
        print "Usage: python cloud_batch.py"
        print "  Will print how many rows in sample database."
        print "Usage: python cloud_batch.py start-row end-row"
        print "  Will send the specified rows in sample database to cloud."
        print ""
        cnt = read_sample_count()
        print "There are", cnt, "rows in the samples database."
        exit(0)

    start = int(sys.argv[1])
    end = int(sys.argv[2])
    print "Selecting data samples", start, "thru", end
    results = get_json_samples(start, end)
    print "Packed result message:", json.dumps(results)
