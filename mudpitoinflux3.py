#!/usr/bin/env python
# from __future__ import unicode_literals
import json
import re
import sys
import redis
import datetime
from influxdb import InfluxDBClient

import logging

LOG_LEVEL = logging.INFO
#LOG_LEVEL = logging.DEBUG
LOG_FILE = "/home/pi/influxMudpi"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)

# influx configuration - edit these
ifuser = "grafana"
ifpass = "enteryourpassword"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086

# connect to influx
ifclient = InfluxDBClient(ifhost, ifport, ifuser, ifpass, ifdb)

# connect to redis
rediscon = "127.0.0.1"

logging.debug("Script Started")
logging.debug(sys.version)

# set redis
r = redis.Redis(rediscon)


# function to flatten JSON
def flatten_json(y):
    out = {}
    logging.debug("start flatten")

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def process():
    ps = r.pubsub()
    # update relay as needed (this only supports 1 relay)
    ps.subscribe('garden/relays/main_water_relay', 'sensors', 'state')
    #    ps.subscribe('sensors')
    logging.debug("Subscribed to PubSub relay and sensors")
    for raw_message in ps.listen():
        logging.debug("Listen Loop")
        logging.debug(raw_message["data"])

        if raw_message["data"] in [1, 2, 3]:
            continue
        jmessage = json.loads(raw_message["data"])

        event = jmessage["event"]
        logging.debug(event)

        if event == "PiSensorUpdate" or event == "SensorUpdate":
            message = jmessage["data"]
            logging.debug("Process")
            logging.debug(message)
            process_message_sensor(flatten_json(message))
        elif (event == "StateChanged") or (event == "Switch"):
            message = jmessage["data"]
            logging.debug("Process")
            logging.debug(message)
            process_message_relay(event, message)
        elif event == "StateUpdated":  # mudpi 0.1
            message = jmessage["new_state"]
            logging.debug("Process - StateUpdated")
            logging.debug(message)
            process_message_state(flatten_json(message))

# Sensor Messages
def process_message_sensor(message):
    logging.debug("Start process_message_sensor")
    logging.debug(message)
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


# Relay
def process_message_relay(event, message):
    time = datetime.datetime.utcnow()
    # print(message)

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

# mudpi v0.10.0 new message format
def process_message_state(message):
    logging.debug("Start process_message_state")
    logging.debug(message)
    time = datetime.datetime.utcnow()

    for d in message:
        # print(d);
        if "state" in d:
            body = [
                {"measurement": message["component_id"] + d[5:],
                 "time": time,
                 "tags": {
                     "sensorname": message["component_id"] + d[5:],
                     "classifier": message["metadata_classifier"]
                 },
                 "fields": {
                     message["component_id"] + d[5:]: message[d]
                 }}
            ]
            logging.debug(body)
            load_influx(body)
            logging.debug("End process_message_state")


# Send to Influx
def load_influx(body):
    # write the measurement
    ifclient.write_points(body)
    logging.debug("SendToInflux")
    
if __name__ == "__main__":
    process()
