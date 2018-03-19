#!python3
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose

def command_input(options={}):
    topics_in=[]
    qos_in=[]

    valid_options=" -b <broker> -p <port>-t <topic> -q QOS -v <verbose> -h
<help>\
-c <loop Time secs -d logging debug  -n Client ID or Name\
-i loop Interval -u Username -P Password\
"
    print_options_flag=False
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hb:i:dk:p:t:q:l:vn:u:P:")
    except getopt.GetoptError:
      print (sys.argv[0],valid_options)
      sys.exit(2)
    qos=0

    for opt, arg in opts:
        if opt == '-h':
            print (sys.argv[0],valid_options)
            sys.exit()
        elif opt == "-b":
             options["broker"] = str(arg)
        elif opt == "-i":
             options["interval"] = int(arg)
        elif opt == "-k":
             options["keepalive"] = int(arg)
        elif opt =="-p":
            options["port"] = int(arg)
        elif opt =="-t":
            topics_in.append(arg)
        elif opt =="-q":
             qos_in.append(int(arg))
        elif opt =="-n":
             options["cname"]=arg
        elif opt =="-d":
            options["loglevel"]="DEBUG"
        elif opt == "-P":
             options["password"] = str(arg)
        elif opt == "-u":
             options["username"] = str(arg)
        elif opt =="-v":
            options["verbose"]=True


    lqos=len(qos_in)
    for i in range(len(topics_in)):
        if lqos >i:
            topics_in[i]=(topics_in[i],int(qos_in[i]))
        else:
            topics_in[i]=(topics_in[i],0)

    if topics_in:
        options["topics"]=topics_in #array with qos
