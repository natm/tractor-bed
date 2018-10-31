#!/usr/bin/env python3

import argparse
import logging
import json
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import socket
LOG = logging.getLogger(__name__)

VERSION = 0.1
BOUNCETIME = 300

HOSTNAME = None
MQTTCLI = None
STARTUP = None
CONFIG = None
DEVICEID = None
client = None

def on_connect(client, data, flags, rc):
    LOG.info("Connected %s", rc)

def on_subscribe(client, userdata, mid, gqos):
    LOG.debug("Subscribed %s", mid)

def on_message(client, userdata, msg):
    pass

def publish_message(suffix, payload, qos=0):
    topic = "tractorbed/%s/%s" % (DEVICEID, suffix)
    client.publish(topic=topic, payload=payload, qos=0)

def job_heartbeat():
    publish_message(suffix="uptime", payload=int(time.time()-STARTUP))

def job_periodic():
    publish_message(suffix="version", payload=VERSION)

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config', required=True)
    args = parser.parse_args()

    LOG.info("Starting v%s", VERSION)

    LOG.info("Reading configuration from %s", args.config)
    global CONFIG
    json_data=open(args.config).read()
    CONFIG = json.loads(json_data)

    global STARTUP
    STARTUP = time.time()

    global HOSTNAME
    HOSTNAME = socket.gethostname().split(".")[0]

    global DEVICEID
    DEVICEID = CONFIG["id"]

    LOG.info("Local device id: %s", DEVICEID)

    LOG.info("Connecting to MQTT")
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.username_pw_set(CONFIG["mqtt"]["username"], CONFIG["mqtt"]["password"])
    LOG.info("connecting to MQTT")
    client.connect(CONFIG["mqtt"]["host"], CONFIG["mqtt"]["port"], 60)

    # setup GPIO

    job_heartbeat()
    job_periodic()

    scheduler = BackgroundScheduler()
    scheduler.add_job(job_heartbeat, 'interval', seconds=30)
    scheduler.start()

    client.loop_forever()


if __name__ == "__main__":
    main()
