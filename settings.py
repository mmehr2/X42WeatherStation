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
    result = "null"
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

def setval(keyname, value, first=False):
    ''' Set a key's value. Exception error if no key of that name exists.
    To avoid exception on first-time creation, set first=True.
    '''
    global dberr
    dbname = wsut.database_filename
    dberr = ""
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
    return dberr

def create(keyname, value):
    return setval(keyname, value, first=True)

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
    # Usage
    argc = len(sys.argv)
    result = 0
    if argc <= 1:
        print "Usage:\tpython %s [keyname [new_value]]" % sys.argv[0]
        print """\

        Will report the value of key with name keyname, OR
        If new_value is present, will set the key to the provided value.
        Wildcards can be used in keyname (%, not *) unless new_value is present.
        If keyname is '%', all values are shown.
        """
        # exit(result)
    
    # Implement usage.
    kname = sys.argv[1] if argc > 1 else "%"
    newval = sys.argv[2] if argc > 2 else "@&@&@"
    if kname != "%":
        result = get(kname)
        #print "Test result =<" + result+ ">"
    if newval != '@&@&@':
        if result != "null":
            result = setval(kname, newval)
            if result == "":
                print "Updated setting", kname, "=", newval
        else:
            result = create(kname, newval)
            if result == "":
                print "Added new setting", kname, "=", newval
            else:
                print "Unable to add new setting", kname, "=", newval
    contents = getall(kname)
    print "Current values of settings:"
    for line in contents:
        (k,v) = line
        print k + "=" + v
    exit(0)
