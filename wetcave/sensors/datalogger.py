import psutil
import paho.mqtt.client as mqtt
import paho.mqtt.properties as properties
from sensors.models import Pressure,Temperature,Range,Rain
from settings.models import MQTTConfig
# from sensors.sensors import SensorCollector
from logging import getLogger
from datetime import datetime,timezone
import os
import time
import signal
import sys
import ssl
import json
logger = getLogger(__name__)

def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    logger.info("Stopping Data subscription")
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

def parse_time(json_dict):
    for (key, value) in json_dict.items():
        if key == "time":
            json_dict[key] = datetime.fromisoformat(value)
    return json_dict


def add_pressure(data):
    item=Pressure.objects.create(pressure=data["value"],pressure_error=data["std"],time=data["time"])

def add_temperature(data):
    item=Temperature.objects.create(temperature=data["value"],temperature_error=data["std"],time=data["time"])

def add_range(data):
    item=Range.objects.create(traveltime=data["value"],traveltime_error=data["std"],time=data["time"])

def add_rain(data):
    item=Rain.objects.create(time=data["time"],validflag=data['valid'])

topicmap={"barotemp/pressure":add_pressure,"barotemp/temp":add_temperature,"range/traveltime":add_range,"tippingbucket/tip":add_rain}

def process_message(client, userdata, message):
    sensortopic=message.topic.removeprefix(userdata["sensortopic"])
    try:
        data=json.loads(message.payload,object_hook=parse_time)
        topicmap[sensortopic](data)
    except:
        if message.topic.endswith(userdata["clientoffline"]):
            if message.payload == b"LOST_CONNECTION":
                tstamp=datetime.now(timezone.utc)
            else:
                tstamp=datetime.fromisoformat(message.payload.decode('utf-8'))
            #insert null entries so connection loss is registered
            item=Pressure.objects.create(time=tstamp)
            item=Temperature.objects.create(time=tstamp)
            item=Range.objects.create(time=tstamp)
            item=Rain.objects.create(time=tstamp,validflag=0)
        else:
            logger.warning(f"No topic mapping found for {message.topic}")

    

def on_connect(client, userdata, flags, reason_code, properties=None):
    logger.info(f"Subscribing to {userdata['sensortopic']}#")
    client.subscribe(topic=userdata["sensortopic"]+"#",qos=userdata["qos"])
    client.subscribe(topic=userdata["clientoffline"],qos=userdata["qos"])

def start_logging():
    #retrieve the MQTT configuration
    mqttconf=MQTTConfig.objects.first()
    transport="tcp"
    clean_start=False
    qos=1
    keepalive=60
    connect_properties = properties.Properties(properties.PacketTypes.CONNECT)
    connect_properties.SessionExpiryInterval = 86400
    client = mqtt.Client(client_id=mqttconf.clientid,transport=transport, 
                         protocol=mqtt.MQTTv5,
                         userdata={"sensortopic":mqttconf.topic+"/sensor/","qos":qos,"clientoffline":f"{mqttconf.topic}/{mqttconf.pubclientid}/offline"})
    
    client.username_pw_set(mqttconf.user,mqttconf.password)
    if mqttconf.usessl:
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED
                       )
    client.on_connect=on_connect
    client.on_message=process_message

    client.connect(mqttconf.broker,port=mqttconf.port,keepalive=keepalive,clean_start=clean_start,properties=connect_properties);
    client.loop_forever() 


def stop_logging():
    pass

# def start_logging(sampling=60):
    # #retrieve the last state of the logger
    # try:
        # laststate=LoggerState.objects.latest('time')
        # if laststate.action != LoggerState.Action.STOP:
            # # restart logging (stop first)
            # stop_logging(laststate)
    # except LoggerState.DoesNotExist:
    # pass #ok when no entry exists yet

    # #create a new start entry for the 
    # newstate=LoggerState(time=datetime.now().astimezone(),action=LoggerState.Action.START,sampling=sampling,pid=os.getpid())
    # newstate.save()
    # sensorscol=SensorCollector()
    # #set very permitting bound for first run
    # ttimeoutlierbound=[800,12000]
    # while True:
        # logger.info("Taking new sensor sample")
        # sdict=sensorscol.sample(ttimeoutlierbound)
        # #Update outlier bound in order to reject outliers falling ca 20cm (2 way) from previous estimate
        # if "traveltime" in sdict:
            # ttimeoutlierbound=[sdict["traveltime"]-500,sdict["traveltime"]+500]
        # sample=SensorData(**sdict)
        # sample.save()
        # time.sleep(sampling)

# def stop_logging(laststate=None):
    # try:    
        # if type(laststate) == type(None):
            # laststate=LoggerState.objects.latest('time')

    # except LoggerState.DoesNotExist:
        # logger.info("Found no registered logging instance")
        # return #Nothing to stop

    # if laststate.action == LoggerState.Action.STOP:
        # logger.info("Logger already stopped")
        # return
    # try:
        # lastprocess = psutil.Process(laststate.pid)
        # logger.info(f"terminating running datalogger process {laststate.pid}")
        # lastprocess.terminate()
        # lastprocess.wait()
    # except psutil.NoSuchProcess:
        # logger.info("Pid not found, nothing to stop, writing stop state")
    # newstat=LoggerState(action=LoggerState.Action.STOP,time=datetime.now().astimezone(),sampling=laststate.sampling,pid=laststate.pid)
    # newstat.save()

