#!python3
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose

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
port=1883
keepalive=60
