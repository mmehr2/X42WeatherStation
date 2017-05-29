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

from kafka import KafkaProducer
from kafka.errors import KafkaError

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
    except KafkaError as e:
        result = "Kafka Producer Init Error %s" % e
    return result

def send(data, topic = default_topic):
    global producer
    result = ""
    try:
        producer.send(topic, data) # returns an async future
        producer.flush() # block until all async messages are sent
    except KafkaError as e:
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
    message = {"test1": 12, "test2": 34}
    print "Sending message X to topic:", default_topic, " X:", json.dumps(message)
    result = send(message)
    print "Result of test send was :", result
    exit(0)
