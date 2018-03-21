#!python3
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose

def convert(t):
    d=""
    for c in t:  # replace all chars outside BMP with a !
            d =d+(c if ord(c) < 0x10000 else '!')
    return(d)

def print_out(m):
    if display:
        print(m)

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
