'''
Cloud send functions.
These are based on Apache Kafka Producer for compatibility with 30454 Class Final Project.
Default topic is: x42ws.public.data

Resources:
   sudo pip install kafka-python

Date: May 24. 2017
Author: Michael L. Mehr
'''

import sys
import settings as dbs
import json
import datetime

import cloud_batch as cbat
import random
import utilities as wsut

from kafka import KafkaProducer
#from kafka.errors import KafkaError

default_port = 9092
default_host = 'ec2-54-149-164-98.us-west-2.compute.amazonaws.com'
default_retries = 3
default_topic = "iotmsgs"
#default_topic = "x42ws.public.data"

def init():
    global producer, port, host, retries
    port = dbs.get('AWS_Port')
    host = dbs.get('AWS_Instance')
    retries = dbs.get('AWS_Retries')
    if port == 'null':
        port = default_port
    if host == 'null':
        host = default_host
    if retries == 'null':
        retries = default_retries
    server1 = '%s:%s' % (host, port)
    #print "Server requested:", server1, "retries", retries
    result = ""
    try:
        producer = KafkaProducer(bootstrap_servers=[server1],\
                                 retries=retries,\
                                 value_serializer=lambda m: json.dumps(m).encode('ascii'))
    except Exception as e:
        result = "Kafka Producer Init Error %s" % e
    return result

def send(data, topic = default_topic):
    global producer
    result = ""
    try:
        producer.send(topic, data) # returns an async future
        producer.flush() # block until all async messages are sent
    except Exception as e:
        result = "Kafka Producer Send Error %s" % e
    return result

if __name__=='__main__':
    global port, host, retries
    print "Starting Apache Kafka Producer with the following configuration:"
    result = init()
    print "  Host:", host
    print "  Port:", port
    print "  Retries:", retries
    if result != "":
        print "Could not start producer: result:", result
        exit(255)
    #message = {"test1": 12, "test2": 34}
    #print "Sending message X to topic:", default_topic, " X:", json.dumps(message)
    #result = send(message)
    #print "Result of test send was :", result
    # Send a random number of data sample messages (up to CloudSendBatchSize)
    start = dbs.get("CloudSendLastRowid")
    if start == "null":
        start = 1
        dbs.create("CloudSendLastRowid", start)
    else:
        start = int(start)
    max_size = dbs.get("CloudSendBatchSize")
    if max_size == "null":
        max_size = 10
    else:
        max_size = int(max_size)
    size1 = max_size/2
    size2 = max_size
    random.seed()
    size = random.randint(size1, size2)
    end = start + size -1
    next = end + 1
    dbcount = cbat.read_sample_count()
    if end > dbcount:
        end = dbcount
        next = 1
        size = end - start + 1
    print "Sending the next", size, "samples", "(%d:%d)" % (start, end), "to the cloud."
    json_message = cbat.get_json_samples(start, end)
    result = send(json_message, topic = wsut.data_topic_name)
    if result == "":
        # successful send, OK to update the settings values
        dbs.setval("CloudSendLastRowid", next)
        print "Updated next row to send to", next
    
    exit(0)
