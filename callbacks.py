#!python3
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose

#THIS FILE DEFINES THE CALLBACKS AND THEN
#INITIALIZES THE MQTT CLIENT OBJECT

#callbacks -all others define in functions module
def on_connect(client, userdata, flags, rc):
    logging.debug("Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id")
    if rc==0:
        client.connected_flag=True
    else:
        client.bad_connection_flag=True

def on_disconnect(client, userdata, rc):
    logging.debug("disconnecting reason  " + str(rc))
    client.connected_flag=False
    client.disconnect_flag=True
    client.subscribe_flag=False

def on_subscribe(client,userdata,mid,granted_qos):
    m="in on subscribe callback result "+str(mid)
    logging.debug(m)
    client.subscribed_flag=True

def on_message(client,userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    message_handler(client,m_decode,topic)
    #print("message received")
    
def message_handler(client,msg,topic):
    data=dict()
    tnow=time.localtime(time.time())
    m=time.asctime(tnow)+" "+topic+" "+msg
    data["time"]=tnow
    data["topic"]=topic
    data["message"]=msg
    if has_changed(topic,msg):
        print("storing changed data",topic, "   ",msg)
        q.put(data) #put messages on queue

def has_changed(topic,msg):
    topic2=topic.lower()
    if topic2.find("control")!=-1:
        return False
    if topic in last_message:
        if last_message[topic]==msg:
            return False
    last_message[topic]=msg
    return True

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
