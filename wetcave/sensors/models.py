from django.db import models


class Pressure(models.Model):
    pressure = models.FloatField("Pressure in hPa",null=True,blank=True)
    pressure_error = models.FloatField("Error of pressure in hPa",null=True,blank=True)
    time = models.DateTimeField("Observation time",db_index=True)

class Temperature(models.Model):
    temperature = models.FloatField("Temperature in degrees Celsius",null=True,blank=True)
    temperature_error = models.FloatField("Error of Temperature in degrees Celsius",null=True,blank=True)
    time = models.DateTimeField("Observation time",db_index=True)

class Range(models.Model):
    traveltime = models.FloatField("2-way traveltime in microseconds",null=True,blank=True)
    traveltime_error = models.FloatField("Error of 2-way traveltime in microseconds",null=True,blank=True)
    time = models.DateTimeField("Observation time",db_index=True)

class Rain(models.Model):
    time = models.DateTimeField("Time of tip event",db_index=True)

# class LoggerState(models.Model):
    # class Action(models.IntegerChoices):
        # START = 1
        # STOP = 2
    # time = models.DateTimeField("Time tag of logging status change")
    # # sampling interval, 0 or empty means no sampling is active
    # sampling=models.IntegerField("Active sampling interval in seconds")
    # action=models.IntegerField("Action which was taken by the sensor logging app",choices=Action.choices)
    # pid=models.IntegerField("PID of process which was started")




