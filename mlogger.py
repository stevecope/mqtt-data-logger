###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
"""
implements data logging class
"""
import time,os,json,logging

###############
class m_logger(object):
    """Class for logging data to a file. You can set the maximim bunber
of messages in a file the default is 1000. When the file is full
a new file is created.Log files are store under a root directoy
and a sub directory that uses the timestamp for the directory name
Log file data is flushed immediately to disk so that data is not lost.
Data can be stored as plain text or in JSON format """
    def __init__(self,log_dir="mlogs",log_recs=1000,number_logs=0):
        self.log_dir=log_dir
        self.log_recs=log_recs
        self.number_logs=number_logs
        self.count=0
        self.log_dir=self.create_log_dir(self.log_dir)
        self.fo=self.get_log_name(self.log_dir,self.count)
        self.new_file_flag=0
        self.writecount=0
        self.timenow=time.time()
        self.flush_flag=True
        self.flush_time=2 #flush logs to disk every 2 seconds
    def __flushlogs(self): # write to disk 
        self.fo.flush()
        #logging.info("flushing logs")
        os.fsync(self.fo.fileno())
        self.timenow=time.time()
    def __del__(self):
        if not self.fo.closed:
            print("closing log file")
            self.fo.close()
    def close_file(self):
        if not self.fo.closed:
            print("closing log file")
            self.fo.close()
    def create_log_dir(self,log_dir):
    """Function for creating new log directories
    using the timestamp for the name"""   
        self.t=time.localtime(time.time())
        
        self.time_stamp=(str(self.t[1])+"-"+str(self.t[2])+"-"+                                          
        str(self.t[3])+"-"+str(self.t[4]))                                                                             
        logging.info("creating sub directory"+str(self.time_stamp))
        try:
            os.stat(self.log_dir)
        except:
            os.mkdir(self.log_dir) 
        self.log_sub_dir=self.log_dir+"/"+self.time_stamp 
        try:
            os.stat(self.log_sub_dir)
        except:
            os.mkdir(self.log_sub_dir)
        return(self.log_sub_dir)

    def get_log_name(self,log_dir,count):
        """get log files and directories"""
        self.log_numbr="{0:003d}".format(count)
        logging.info("s is"+str(self.log_numbr))
        self.file_name=self.log_dir+"/"+"log"+self.log_numbr
        logging.info("creating log file "+self.file_name)
        f = open(self.file_name,'w') #clears file if it exists
        f.close()
        f=open(self.file_name, 'a')
        return(f)
    def log_json(self,data):
        jdata=json.dumps(data)+"\n"
        self.log_data(jdata)                                                                                          
                                                                                         
    def log_data(self, data):
        self.data=data
        try:
            self.fo.write(data)
            self.writecount+=1
            self.__flushlogs()
            if self.writecount>=self.log_recs:
                self.count+=1 #counts number of logs
                if self.count>self.number_logs and self.number_logs !=0 :
                      logging.info("too many logs: starting from 0")
                      self.count=0 #reset
                self.fo=self.get_log_name(self.log_dir,self.count)
                self.writecount=0
        except BaseException as e:
            logging.error("Error on_data: %s" % str(e))
            return False
        return True

