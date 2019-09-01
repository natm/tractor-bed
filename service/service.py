#!/usr/bin/env python3

import argparse
import logging
import json
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import paho.mqtt.client as mqtt
import wiringpi
import RPi.GPIO as GPIO
import Adafruit_DHT
import pygame
import socket
import sys
from apscheduler.schedulers.background import BackgroundScheduler

LOG = logging.getLogger(__name__)

VERSION = 0.2
BOUNCETIME = 300

HOSTNAME = None
MQTTCLI = None
STARTUP = None
CONFIG = None
DEVICEID = None
client = None

PIN_DHT = 4

BUTTON_1 = 29
BUTTON_2 = 31
BUTTON_3 = 33
BUTTON_4 = 22
BUTTON_5 = 37
BUTTONS = [
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    BUTTON_5
]

OUTPUTS = {
    "ledpower": { "addr": 73, "off": 0, "on": 1 },
    "led1": { "addr": 74, "off": 0, "on": 1 },
    "led2": { "addr": 75, "off": 0, "on": 1 },
    "led3": { "addr": 76, "off": 0, "on": 1 },
    "relay1": { "addr": 65, "off": 1, "on": 0},
    "relay2": { "addr": 66, "off": 1, "on": 0},
    "relay3": { "addr": 67, "off": 1, "on": 0},
    "relay4": { "addr": 68, "off": 1, "on": 0},
    "relay5": { "addr": 69, "off": 1, "on": 0},
    "relay6": { "addr": 70, "off": 1, "on": 0},
    "relay7": { "addr": 71, "off": 1, "on": 0},
    "relay8": { "addr": 72, "off": 1, "on": 0}
}

class Output(object):


    @staticmethod
    def setup(name):
        definition = OUTPUTS[name]
        addr = definition["addr"]
        wiringpi.pinMode(addr, 1)

    @staticmethod
    def on(name):
        Output.state_set(name=name, mode="on")

    @staticmethod
    def off(name):
        Output.state_set(name=name, mode="off")

    @staticmethod
    def state_set(name, mode):
        definition = OUTPUTS[name]
        addr = definition["addr"]
        wiringpi.digitalWrite(addr, definition[mode])
        suffix = "outputs/stat/%s" % (name)
        publish_message(suffix=suffix, payload=mode.upper())

    @staticmethod
    def set_from_mqtt(topic, payload):
        for name, definition in OUTPUTS.items():
            if topic.endswith("/%s" % (name)):
                Output.state_set(name=name, mode=payload.lower())


def on_connect(client, data, flags, rc):
    LOG.info("Connected %s", rc)

def on_subscribe(client, userdata, mid, gqos):
    LOG.info("Subscribed %s", mid)

def on_message(client, userdata, msg):
    # LOG.info("Message: %s %s", msg.topic, msg.payload)
    if msg.topic.endswith("/service/cmnd/reset"):
        LOG.info("Reset requested via MQTT")
        sys.exit(1)
    elif "/outputs/cmnd/" in str(msg.topic):
        Output.set_from_mqtt(topic=msg.topic, payload=msg.payload.decode('utf-8'))

def publish_message(suffix, payload, qos=0):
    topic = "tractorbed/%s/%s" % (DEVICEID, suffix)
    client.publish(topic=topic, payload=payload, qos=0)

def job_heartbeat():
    publish_message(suffix="uptime", payload=int(time.time()-STARTUP)/60)
    Output.off(name="ledpower")
    time.sleep(0.2)
    Output.on(name="ledpower")

def job_periodic():
    publish_message(suffix="version", payload=VERSION)

def job_temperature():
    humidity, temperature = Adafruit_DHT.read_retry(22, PIN_DHT)
    publish_message(suffix="humidity", payload=humidity)
    publish_message(suffix="temperature", payload=temperature)

def interupt_button_pressed(channel):
    LOG.info("pressed %s", channel)

def init_io():
    humidity, temperature = Adafruit_DHT.read_retry(22, PIN_DHT)
    LOG.info("Humidity %s", humidity)

    # setup buttons
    GPIO.setmode(GPIO.BOARD)
    for pin in BUTTONS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=interupt_button_pressed, bouncetime=BOUNCETIME)

    # mcp23017 for outputs
    pin_base = 65       # lowest available starting number is 65
    i2c_addr = 0x20     # A0, A1, A2 pins all wired to GN
    wiringpi.wiringPiSetup()                    # initialise wiringp
    wiringpi.mcp23017Setup(pin_base,i2c_addr)   # set up the pins and i2c address

    for key, definition in OUTPUTS.items():
        Output.setup(name=key)
        Output.off(name=key)

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
    client.connect(CONFIG["mqtt"]["host"], CONFIG["mqtt"]["port"], 60)
    client.subscribe("tractorbed/%s/outputs/cmnd/#" % (DEVICEID))
    client.subscribe("tractorbed/%s/service/cmnd/#" % (DEVICEID))

    # setup GPIO
    init_io()

    job_heartbeat()
    job_periodic()

    scheduler = BackgroundScheduler()
    scheduler.add_job(job_heartbeat, 'interval', seconds=5)
    scheduler.add_job(job_temperature, 'interval', seconds=30)
    scheduler.start()

    # turn on the power LED
    Output.on(name="ledpower")

    client.loop_forever()


if __name__ == "__main__":
    main()


