'''
Cloud receive functions.
These are based on Apache Kafka Consumer for compatibility with 30454 Class Final Project.
Default topic is: x42ws.public.commands

Resources:
   sudo pip install kafka-python

Date: May 31. 2017
Author: Michael L. Mehr
'''

import sys
import settings as dbs
import json
import datetime

from kafka import KafkaConsumer

default_port = 9092
default_host = 'ec2-54-149-164-98.us-west-2.compute.amazonaws.com'
default_timeout = 10000 # msec
default_topic = "iotmsgs"
#default_topic = "x42ws.public.commands"

def init(topic = default_topic):
    global consumer, port, host, timeout, topicname
    topicname = topic
    port = dbs.get('AWS_Port')
    host = dbs.get('AWS_Instance')
    timeout = dbs.get('AWS_ConsumerTimeout')
    if port == 'null':
        port = default_port
    if host == 'null':
        host = default_host
    if timeout == 'null':
        timeout = default_timeout
    server1 = '%s:%s' % (host, port)
    #print "Server requested:", server1
    result = ""
    try:
        consumer = KafkaConsumer(topic,\
                                 bootstrap_servers=[server1],\
                                 consumer_timeout_ms=timeout,\
                                 auto_offset_reset='earliest',\
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')))
    except Exception as e:
        result = "Kafka Consumer Init Error %s" % e
    return result

def receive():
    global consumer
    result = {}
    try:
        for msg in consumer:
            result += msg
    except Exception as e:
        result += {"error": "Kafka Consumer Send Error %s" % e}
    return result

if __name__=='__main__':
    global port, host, timeout, topicname
    print "Starting Apache Kafka Consumer with the following configuration:"
    result = init()
    print "  Host:", host
    print "  Port:", port
    print "  Timeout(s):", timeout/1000.0
    if result != "":
        print "Could not start consumer: result:", result
        exit(255)
    print "Consumer awaiting messages on topic", topicname, ":"
    data = receive()
    print "Data:", json.dumps(data, sort_keys=True,
                              indent=4, separators=(',', ': '))
    exit(0)
