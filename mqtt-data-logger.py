#!python3
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
"""
This will log messages to file.Los time,message and topic as JSON data
"""
mqttclient_log=False #MQTT client logs showing messages
Log_worker_flag=True
import paho.mqtt.client as mqtt
import json
import os
import time
import sys, getopt,random
import logging
import mlogger as mlogger
import threading
from queue import Queue
from mqtt_functions import *
from command import command_input
import command
#from utilities import convert, print_out


q=Queue()
##helper functions
def convert(t):
    d=""
    for c in t:  # replace all chars outside BMP with a !
            d =d+(c if ord(c) < 0x10000 else '!')
    return(d)
###

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

# MAIN PROGRAM
options=command.options

if __name__ == "__main__" and len(sys.argv)>=2:
    options=command_input(options)
else:
    print("Need broker name and topics to continue.. exiting")
    raise SystemExit(1)

#verbose=options["verbose"]

if not options["cname"]:
    r=random.randrange(1,10000)
    cname="logger-"+str(r)
else:
    cname="logger-"+str(options["cname"])
log_dir=options["log_dir"]
log_records=options["log_records"]
number_logs=options["number_logs"]
log=mlogger.m_logger(log_dir,log_records,number_logs)
print("Log Directory =",log_dir)
print("Log records per log =",log_records)
if number_logs==0:
    print("Max logs = Unlimited")
else:
    print("Max logs  =",number_logs)
    
#log=mlogger.m_logger()

#Initialise_client_object() # add extra flags
logging.info("creating client"+cname)
Initialise_client_object()#create flags
client=Initialise_clients(cname,mqttclient_log,False)#create and initialise client object
topics=options["topics"]
broker=options["broker"]
port=options["port"]

if options["username"] !="":
    client.username_pw_set(options["username"], options["password"])

if options["storechangesonly"]:
    print("starting storing only changed data")
else:
    print("starting storing all data")
    
##
#Log_worker_flag=True
t = threading.Thread(target=log_worker) #start logger
t.start() #start logging thread
###

client.last_message=dict()
client.q=q #make queue available as part of client


#loop and wait until interrupted
try:
    run_loop(client,broker,port,topics)

except KeyboardInterrupt:
    print("interrrupted by keyboard")


Log_worker_flag=False #stop logging thread
time.sleep(5)

