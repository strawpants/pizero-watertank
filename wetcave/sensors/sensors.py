from .hp206c import hp206c
import RPi.GPIO as GPIO
import sys
import time
from logging import getLogger
from statistics import mean,stdev
from datetime import datetime
from math import sqrt
usleep = lambda x: time.sleep(x*1e-6)
logger=getLogger(__name__)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

class SensorCollector:
    sounderpin=24
    nbarosamples=10
    nsoundersamples=15
    def __init__(self):
        self.pres_temp=hp206c()
        ret=self.pres_temp.isAvailable()
        if self.pres_temp.OK_HP20X_DEV == ret:
            logger.info("Barometer is available.")
        else:
            logger.info("Barometer isn't availablei, disabling")
            self.pres_temp=None
        
        #setup ultrasounder
        GPIO.setmode(GPIO.BCM)
        time.sleep(1)
    
    def __del__(self):
        logger.info("Cleanup of GPIO")
        GPIO.cleanup()

    def sampleBaro(self):
            pres=None
            temp=None
            presstd=None
            tempstd=None
            if self.pres_temp:
                preslist=[]
                templist=[]
                for i in range(self.nbarosamples+1):
                    p=self.pres_temp.ReadPressure()
                    if (p < 600):
                        #sometimes the first measurement is wrong
                        continue
                    t=self.pres_temp.ReadTemperature()
                    
                    preslist.append(p)
                    templist.append(t)
                
                error_scale=1.0/sqrt(len(preslist)) 
                pres=mean(preslist)
                temp=mean(templist)
                presstd=stdev(preslist)*error_scale
                tempstd=stdev(templist)*error_scale

            return {"pressure":pres,"temperature":temp,"pressure_error":presstd,"temperature_error":tempstd}

    def sampleRangeSingle(self):
        GPIO.setup(self.sounderpin, GPIO.OUT)
        GPIO.output(self.sounderpin,GPIO.LOW)
        usleep(2)
        GPIO.output(self.sounderpin,GPIO.HIGH)
        usleep(10)
        GPIO.output(self.sounderpin,GPIO.LOW)
        GPIO.setup(self.sounderpin, GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if GPIO.input(self.sounderpin):
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not GPIO.input(self.sounderpin):
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            dt=None
        traveltime=t2-t1
        return traveltime*1e6

    def sampleRange(self,outlierbounds=[800,12000]):
        dtlist=[]
        for i in range(self.nsoundersamples+1):
            dt=self.sampleRangeSingle()
            if dt == None:
                #try again
                continue
            if dt < outlierbounds[0] or dt > outlierbounds[1]:
                #outlier don't use in the computation of the mean
                continue
            dtlist.append(dt)
        error_scale=1.0/sqrt(len(dtlist)) 
        return {"traveltime":mean(dtlist),"traveltime_error":stdev(dtlist)* error_scale}

    def sample(self,traveltime_outlierbounds=None):
        sensordict=self.sampleBaro()
        sensordict.update(self.sampleRange(traveltime_outlierbounds))
        sensordict["epoch"]=datetime.now().astimezone()
        return sensordict
