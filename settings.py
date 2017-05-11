'''
Access to persistent settings.
Author: Michael L. Mehr
Date: May 9, 2017
Project: Weather Station v1.0
'''

import sys
import sqlite3
import utilities as wsut

dberr = "" # Exception error strings go here. Check if curious ;)

def get(keyname):
    ''' Retrieve a key's value. Returns empty string if no key of that name exists. '''
    dbname = wsut.database_filename
    global dberr
    result = ""
    dberr = ""
    try:
        conn = sqlite3.connect(dbname)
        #print "Opened database", dbname
        curs = conn.cursor()
        results = curs.execute("SELECT * FROM settings WHERE stgkey = (?)", (keyname,))
        for (K,V) in results:
            if K == keyname:
                result = V
    except:
        e = sys.exc_info()[0]
        print("Error on settings database extraction: %s" % e)
        dberr = "Get error %s" % e
    finally:
        #print "Closing database ", dbname
        conn.close()
    return result

def set(keyname, value, first=False):
    ''' Set a key's value. Exception error if no key of that name exists.
    To avoid exception on first-time creation, set first=True.
    '''
    global dberr
    dbname = wsut.database_filename
    try:
        conn = sqlite3.connect(dbname)
        #print "Opened database", dbname
        curs = conn.cursor()
        if first:
            print "Exec INSERT", keyname, value
            curs.execute("INSERT INTO 'settings' VALUES((?), (?))", (keyname, value))
        else:
            print "Exec UPDATE", value, keyname
            curs.execute("UPDATE 'settings' SET stgval = (?) WHERE stgkey = (?)", (value, keyname))
        conn.commit()
    except:
        e = sys.exc_info()[0]
        print("Error on settings database insertion: %s" % e)
        dberr = "Get error %s" % e
    finally:
        #print "Closing database ", dbname
        conn.close()
    return

def create(keyname, value):
    return set(keyname, value, first=True)

def getall(keyslike):
    ''' Retrieve a key's value. Returns empty string if no key of that name exists. '''
    dbname = wsut.database_filename
    global dberr
    result = []
    dberr = ""
    try:
        conn = sqlite3.connect(dbname)
        #print "Opened database", dbname
        curs = conn.cursor()
        results = curs.execute("SELECT * FROM 'settings' WHERE stgkey LIKE (?)", (keyslike,))
        result = [[K,V] for (K,V) in results]
    except:
        e = sys.exc_info()[0]
        print("Error on settings database total extraction: %s" % e)
        dberr = "Get error %s" % e
    finally:
        #print "Closing database ", dbname
        conn.close()
    return result

if __name__=="__main__":
    print "Using 'settings' table of ", wsut.database_filename
    # Create some defaults here to make this script useful.
    sval = '128'
    val = get('CameraLightThreshold')
    print "Original CameraLightThreshold = ", val
    if len(sys.argv) > 1:
        sval = sys.argv[1]
        set('CameraLightThreshold', sval)
        val = get('CameraLightThreshold')
        if val != sval:
            print "Got value error creating CameraLightThreshold:<%s> from %s" % (val, sval)
        else:
            print "Properly set CameraLightThreshold to ", val
    # Show what we've got now
    contents = getall("%")
    print "Current settings database:"
    print contents
