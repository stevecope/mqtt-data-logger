Simple Python MQTT Data Logger

This software uses the Python logger to create a logfile
for all messages for all topics to which this MQTT client
has subscribed.
Note: by default it will only log changed messages. This is for sensors 
that send out their state a regular intervals but that state doesn't change
The program is run from the command line
You can subscribe to multiple topics.




You need to provide the script with:

    List of topics to monitor
    broker name and port
    username and password if needed.
    base log directory and number of logs have defaults
Valid command line Options:
--help <help>
-h <broker> 
-b <broker> 
-p <port>
-t <topic> 
-q <QOS>
-v <verbose>
-d logging debug 
-n <Client ID or Name>
-u Username 
-P Password
-s <store all data>\
-l <log directory default= mlogs> 
-r <number of records default=100>\
-f <number of log files default= unlimited"

	Example Usage:

You will always need to specify the broker name or IP address 
and the topics to log

Note: you may not need to use the python prefix or may 
need to use python3 mqtt_data_logger.py (Linux)

Specify broker and topics 

    python mqtt_data_logger.py -b 192.168.1.157 -t sensors/#

Specify broker and multiple topics

    python mqtt_data_logger.py -b 192.168.1.157 -t sensors/# -t  home/#
	

Log All Data:

    python mqtt_data_logger.py b 192.168.1.157 -t sensors/# -s 

Specify the client name used by the logger

    python mqtt_data_logger.py b 192.168.1.157 -t sensors/# -n data-logger

Specify the log directory

    python mqtt_data_logger.py b 192.168.1.157 -t sensors/# -l mylogs
 
---------
Logger Class

The class is implemented in a module called m_logger.py (message logger).

To create an instance you need to supply three parameters:

    The log directory- defaults to mlogs
    Number of records to log per log- defaults to 5000
    Number of logs. 0 for no limit.- defaults to 0

log=m_logger(log_dir="logs",log_recs=5000,number_logs=0):

The logger creates the log files in the directory using the current date and time for the directory names.

The format is month-day-hour-minute e.g.


You can log data either in plain text format or JSON format.

To log data either in plain text then use the

    log_data(data) method.

To log data as JSON encoded data call the

    log_json(data) method.

Both method takes a single parameter containing the data to log as a string, list or dictionary..

e.g.

log.log_data(data) 
or
log.log_json(data)

#The log file will contain the data as 
#plain text or  JSON encoded data strings
#each on a newline.

The logger will return True if successful and False if not.

To prevent loss of data in the case of computer failure the logs are continuously flushed to disk .
 
 Read more about this application here:
http://www.steves-internet-guide.com/simple-python-mqtt-data-logger/
