#!/usr/bin/env python
#from __future__ import unicode_literals
import json
import re
import sys
import redis
import datetime
from influxdb import InfluxDBClient

import logging

LOG_LEVEL = logging.INFO
#LOG_LEVEL = logging.DEBUG
LOG_FILE = "/home/pi/mylogv2"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)

# influx configuration - edit these
ifuser = "grafana"
ifpass = "enteryourpassword"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
  
# connect to redis
rediscon = "127.0.0.1"

logging.debug("Script Started")
logging.debug(sys.version)

#set redis
r = redis.Redis(rediscon)


def process():
    ps = r.pubsub()
    ps.subscribe('garden/pi/relays/1', 'sensors') #update relay as needed (this only supports 1 relay)
#    ps.subscribe('sensors') 
    logging.debug("Subscribed to PubSub relay and sensors")
    for raw_message in ps.listen():
        logging.debug("Listen Loop")
        logging.debug(raw_message["data"])

        if raw_message["data"] in [1,2]:
                continue
        jmessage = json.loads(raw_message["data"])
        
        event = jmessage["event"]
        logging.debug(event)

        message = jmessage["data"]
        logging.debug("Process")
        logging.debug(message)
        
        if event == "PiSensorUpdate": 
            process_message( message)
        elif event == "SensorUpdate":
            process_message_soil( message)
        elif (event == "StateChanged") or (event == "Switch"):
            process_message_relay(event, message)

#Relay 
def process_message_relay(event, message):
    time = datetime.datetime.utcnow()
    print(message)

    logging.debug("relayloop")
    body = [
                {"measurement": "relay_" + event.lower(),
                "time": time,
                "tags": {
                    "sensorname": "relay1"
                },
                "fields": {
                   "data": message
                }}
            ]
    logging.debug("process_message")
    logging.debug(body)
    load_influx(body) 

#Pi Sensors (multi Measurements)
def process_message(message):
    time = datetime.datetime.utcnow()

    for d in message:
    #print(d)
        for e in message[d]:
            body = [
                {"measurement": e,
                "time": time,
                "tags": {
                    "sensorname": d
                },
                "fields": {
                    e: message[d][e]
                }}
            ]
            logging.debug("process_message")
            logging.debug(body)
            load_influx(body) 

#Arduino Sensor (single measurement)
def process_message_soil(message):
   # measurement_name = "soil"
    time = datetime.datetime.utcnow()

    for d in message:
            body = [
                {"measurement": d,
                "time": time,
                "tags": {
                    "sensorname": d
                },
                "fields": {
                    d: message[d]
                }}
            ]

            logging.debug("process_message")
            logging.debug(body)
            load_influx(body) 

 

#Send to Influx
def load_influx(body):
    # write the measurement
    ifclient.write_points(body)
    logging.debug("SendToInflux")
    
if __name__ == "__main__":
    process()
