"""
Pubnub cloud interface

Functions desired:
0. Initialize the client interface
1. Send data message
2. Receive control message (setup a callback)
"""

import sys, time
from pubnub.pubnub import PubNubAsyncio as PubNub
from pubnub.pnconfiguration import PNConfiguration
#import settings as dbs

_channelName="my_channel"

def init(channelName):
    ''' Initialize interface to Pubnub messaging system'''
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = "sub-c-d8dabcae-3a72-11e7-b860-02ee2ddab7fe"
    pnconfig.publish_key = "pub-c-e59f81be-15a4-4ebb-a05b-8eebe1602c85"
    pnconfig.ssl = False
    global pubnub
    pubnub = PubNub(pnconfig)
    global _channelName
    _channelName = channelName
    print "Init WS channel ", _channelName
    subscribe(_channelName)

def publish_callback(result, status):
    print "Message publish callback: result=", result, ", status=", status
    # handle publish result, status always present, result if successful
    # status.isError to see if error happened
 
def publish(channelName, data):
    pubnub.publish().channel(_channelName).message(data)\
        .should_store(True).use_post(True).async(publish_callback)

class WSListener(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print "Connected WS channel ", _channelName
        if status.category == PNStatusCategory.PNDisconnectedCategory:
            print "Disconnected WS channel ", _channelName
 
    def message(self, pubnub, message):
        print "Received message on channel ", _channelName, message
 
    def presence(self, pubnub, presence):
        pass

def subscribe(channelName):
    listener = WSListener()
    pubnub.add_listener(listener)
    pubnub.subscribe().channels(channelName).execute()

if __name__=="__main__":
    if len(sys.argv) == 1:
        print """Usage\
        pubnub channelName
        """
    cn = sys.argv[1]
    init(cn)
