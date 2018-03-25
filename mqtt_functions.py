#!python3
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose

#THIS FILE DEFINES THE CALLBACKS AND THEN
#INITIALIZES THE MQTT CLIENT OBJECT
#And contains connection functions and client loops
import paho.mqtt.client as mqtt
import logging,time,command
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
    for t in client.topic_ack:
        if t[1]==mid:
            t[2]=1 #acknowledged
            m="subscription acknowledged  "+str(t[0])
            logging.debug(m)

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
    if command.options["storechangesonly"]:
        if has_changed(client,topic,msg):
            client.q.put(data) #put messages on queue
    else:
        client.q.put(data) #put messages on queue

def has_changed(client,topic,msg):
    topic2=topic.lower()
    if topic2.find("control")!=-1:
        return False
    if topic in client.last_message:
        if client.last_message[topic]==msg:
            return False
    client.last_message[topic]=msg
    return True
#################

def Initialise_client_object():
    mqtt.Client.last_pub_time=time.time()
    mqtt.Client.topic_ack=[]
    mqtt.Client.run_flag=True
    mqtt.Client.subscribe_flag=False
    mqtt.Client.bad_connection_flag=False
    mqtt.Client.connected_flag=False
    mqtt.Client.disconnect_flag=False
    mqtt.Client.disconnect_time=0.0
    mqtt.Client.pub_msg_count=0

def Initialise_clients(cname,mqttclient_log,cleansession=True):
    #flags set
    client= mqtt.Client(cname,cleansession)
    if mqttclient_log: #enable mqqt client logging
        client.on_log=on_log
    client.on_connect= on_connect        #attach function to callback
    client.on_message=on_message        #attach function to callback
    client.on_disconnect=on_disconnect
    client.on_subscribe=on_subscribe
    return client

##################


def run_loop(client,broker,port,topics,keepalive=60,loop_function=None,\
             loop_delay=1,run_forever=False):
    """runs a loop that will auto reconnect and subscribe to topics
    pass topics as a list of tuples
    """
    client.run_flag=True
    no_sub_flag=False
    sub_count=0
    #print("running loop")
    if topics=="": #not subscribing
        no_sub_flag=True
    while client.run_flag: #loop forever

        if client.bad_connection_flag:
            break         
        if not client.connected_flag:
            if Connect(client,broker,port,keepalive,run_forever) !=-1:
                if not wait_for(client,"CONNACK"):
                   client.run_flag=False #break
            else:
                client.run_flag=False #break
        if not no_sub_flag and not client.subscribe_flag and client.connected_flag:
            if subscribe_topics(client,topics)!=-1 and check_subs(client):
                client.subscribe_flag=True
                sub_count=0
                        
            else:# try 3 times to subsribe then quit
                sub_count+=1;
                if sub_count>3:
                    client.run_flag=False

        client.loop(0.01)

        if client.connected_flag and loop_function and client.subscribe_flag: #function to call
                loop_function(client,loop_delay) #call function
    client.disconnect()
    client.connected_flag=False
#This function needs to run inside a loop
def client_loop(client,broker,port=1883,topics="",\
                keepalive=60,subscribe_flag=False,run_forever=False):
    #handles connects and reconnects and subscribes need to be called
    #inside a loop
    no_sub_flag=False
    if topics=="":
        no_sub_flag=True #don't try to subscribe
    client.loop(0.01) #manually call loop
    if not client.connected_flag:
        if Connect(client,broker,port,keepalive,run_forever) !=-1:
            if not wait_for(client,"CONNACK"):
               return False
        else:
            return False
    if client.bad_connection_flag:
        run_flag=False
        return False

         ###handle subscribing after failure
    if not no_sub_flag and not client.subscribe_flag and client.connected_flag:
        if subscribe_topics(client,topics)!=-1 and check_subs(client):
           client.subscribe_flag=True
        else:
            return False
    return True


############



def subscribe_topics(client,topics,qos=0):
   #print("topic ",topics,"  ",qos)
   
   if type(topics) is not list: #topics should be list of tuples
      if type(topics) is not tuple: #topics isn't tuple?
         topic_list=[(topics,qos)]
      else:
         topic_list=[topics]
   else:
      topic_list=topics
   try:
      r=client.subscribe(topic_list)
      if r[0]==0:
          logging.info("subscribed to topic"+str(topic_list)+" return code" +str(r))
          client.topic_ack.append([topic_list,r[1],0]) #keep track of subscription

      else:
          logging.info("error on subscribing "+str(r))
          print("error on subscribing "+str(r))
          return -1

   except Exception as e:
      logging.info("error on subscribe"+str(e))
      return -1
   return r
         
def check_subs(client):
    wcount=0
    while wcount<10:
        for t in client.topic_ack:
            wcount+=1
            if t[2]==0:
                logging.info("subscription to "+str(t[0]) +" not acknowledged")
                break
            print("All subs acknowledged")
            return True
        time.sleep(1)
        if not client.running_loop:
            client.loop(.01)  #check for messages manually

    return False



def Connect(client,broker,port,keepalive,run_forever=False):
    """Attempts connection set delay to >1 to keep trying
    but at longer intervals  """
    connflag=False
    delay=5
    #print("connecting ",client)
    badcount=0 # counter for bad connection attempts
    while not connflag:
        logging.info("connecting to broker "+str(broker))
        print("connecting to broker "+str(broker)+":"+str(port))
        print("Attempts ",badcount)
        time.sleep(delay)
        try:
            res=client.connect(broker,port,keepalive)      #connect to broker
            if res==0:
                connflag=True
                return 0
            else:
                logging.debug("connection failed ",res)
                badcount +=1
                if badcount>=3 and not run_forever: 
                    return -1
                    raise SystemExit #give up
                elif run_forever and badcount<3:
                    delay=5
                else:
                    delay=30

        except:
            client.badconnection_flag=True
            logging.debug("connection failed")
            badcount +=1
            if badcount>=3 and not run_forever: 
                return -1
                raise SystemExit #give up
            elif run_forever and badcount<3:
                delay=5*badcount
            elif delay<300:
                delay=30*badcount

                
    return 0
    #####end connecting

def wait_for(client,msgType,period=.25,wait_time=40,running_loop=False):
    #running loop is true when using loop_start or loop_forever
    client.running_loop=running_loop #
    wcount=0  
    while True:
        logging.info("waiting"+ msgType)
        if msgType=="CONNACK":
            if client.on_connect:
                if client.connected_flag:
                    return True
                if client.bad_connection_flag: #
                    return False
                
        if msgType=="SUBACK":
            if client.on_subscribe:
                if client.suback_flag:
                    return True
        if msgType=="MESSAGE":
            if client.on_message:
                if client.message_received_flag:
                    return True
        if msgType=="PUBACK":
            if client.on_publish:        
                if client.puback_flag:
                    return True
     
        if not client.running_loop:
            client.loop(.01)  #check for messages manually
        time.sleep(period)
        #print("loop flag ",client.running_loop)
        wcount+=1
        if wcount>wait_time:
            print("return from wait loop taken too long")
            return False
    return True
