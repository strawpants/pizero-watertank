import psutil
from sensors.models import LoggerState,SensorData
from sensors.sensors import SensorCollector
from logging import getLogger
from datetime import datetime
import os
import time
import signal
import sys
logger = getLogger(__name__)

def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    logger.info("Stopping datalogger")
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

def start_logging(sampling=60):
    #retrieve the last state of the logger
    try:
        laststate=LoggerState.objects.latest('time')
        if laststate.action != LoggerState.Action.STOP:
            # restart logging (stop first)
            stop_logging(laststate)
    except LoggerState.DoesNotExist:
        pass #ok when no entry exists yet

    #create a new start entry for the 
    newstate=LoggerState(time=datetime.now().astimezone(),action=LoggerState.Action.START,sampling=sampling,pid=os.getpid())
    newstate.save()
    sensorscol=SensorCollector()
    while True:
        logger.info("Taking new sensor sample")
        sdict=sensorscol.sample()
        sample=SensorData(**sdict)
        sample.save()
        time.sleep(sampling)

def stop_logging(laststate=None):
    try:    
        if type(laststate) == type(None):
            laststate=LoggerState.objects.latest('time')

    except LoggerState.DoesNotExist:
        logger.info("Found no registered logging instance")
        return #Nothing to stop

    if laststate.action == LoggerState.Action.STOP:
        logger.info("Logger already stopped")
        return
    try:
        lastprocess = psutil.Process(laststate.pid)
        logger.info(f"terminating running datalogger process {laststate.pid}")
        lastprocess.terminate()
        lastprocess.wait()
    except psutil.NoSuchProcess:
        logger.info("Pid not found, nothing to stop, writing stop state")
    newstat=LoggerState(action=LoggerState.Action.STOP,time=datetime.now().astimezone(),sampling=laststate.sampling,pid=laststate.pid)
    newstat.save()

