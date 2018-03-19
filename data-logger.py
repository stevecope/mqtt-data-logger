#!python3
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
"""
This will log messages to file.Los time,message and topic as JSON data
"""
import paho.mqtt.client as mqtt
import json
import os
import time
import sys, getopt,random
import logging
import classes.mlogger as mlogger
import threading
from queue import Queue
from .callbacks import *

q=Queue()
#from mqtt_functions import *

##### User configurable data section
username=""
password=""
verbose=False #True to display all messages, False to display only changed
messages
mqttclient_log=False #MQTT client logs showing messages
logging.basicConfig(level=logging.INFO) #error logging
#use DEBUG,INFO,WARNING
####
options=dict()

##EDIT HERE ###############
brokers=["192.168.1.157","192.168.1.186","192.168.1.206","192.168.1.185",\
         "test.mosquitto.org","broker.hivemq.com","iot.eclipse.org"]
options["broker"]=brokers[4]
options["port"]=1883
options["verbose"]=True
options["cname"]=""
options["topics"]=[("$SYS/#",0)]
options["topics"]=[("bbc/#",0),("homeautomation",0),("/HomeCtrl",0),\
                   ("/hometest",0)]
options["topics"]=[("steves-house/#",0)]
###
cname=""
sub_flag=""
timeout=60
messages=dict()
last_message=dict()




def log_worker():
    """runs in own thread to log data"""
    while Log_worker_flag:
        while not q.empty():
            results = q.get()
            if results is None:
                continue
            log.log_json(results)
            #print("message saved ",results["message"])
    log.close_file()

########################
####


def Initialise_clients(cname,cleansession=True):
    #flags set
    client= mqtt.Client(cname)
    if mqttclient_log: #enable mqqt client logging
        client.on_log=on_log
    client.on_connect= on_connect        #attach function to callback
    client.on_message=on_message        #attach function to callback
    client.on_disconnect=on_disconnect
    client.on_subscribe=on_subscribe
    return client
###



###########
def convert(t):
    d=""
    for c in t:  # replace all chars outside BMP with a !
            d =d+(c if ord(c) < 0x10000 else '!')
    return(d)
def print_out(m):
    if display:
        print(m)


########################main program
if __name__ == "__main__" and len(sys.argv)>=2:
    command_input(options)
    pass
verbose=options["verbose"]

if not options["cname"]:
    r=random.randrange(1,10000)
    cname="logger-"+str(r)
else:
    cname="logger-"+str(options["cname"])



#log=mlogger.m_logger(log_dir,log_recs,number_logs)
log=mlogger.m_logger()

if username !="":
    client1.username_pw_set(username, password)


#Initialise_client_object() # add extra flags
logging.info("creating client"+cname)
client=Initialise_clients(cname,False)#create and initialise client object
topics=options["topics"]
broker=options["broker"]
port=1883
keepalive=60
print("starting")
##
t = threading.Thread(target=log_worker) #start logger
Log_worker_flag=True
t.start() #start logging thread
###
client.connected_flag=False # flag for connection
client.bad_connection_flag=False
client.subscribed_flag=False
client.loop_start()
client.connect(broker,port)
while not client.connected_flag: #wait for connection
    time.sleep(1)
    print("waiting")
client.subscribe(topics)
while not client.subscribed_flag: #wait for connection
    time.sleep(1)
    print("waiting for subscribe")
print("subscribed ",topics)
#loop and wait until interrupted
try:
    while True:
        pass
except KeyboardInterrupt:
    print("interrrupted by keyboard")


client.loop_stop()  #final check for messages
time.sleep(5)
Log_worker_flag=False #stop logging thread
print("ending ")

