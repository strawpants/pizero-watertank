from django.db import models

class SensorData(models.Model):
    traveltime = models.FloatField("2-way traveltime in microseconds")
    traveltime_error = models.FloatField("Error of 2-way traveltime in microseconds")
    pressure = models.FloatField("Pressure in hPa")
    pressure_error = models.FloatField("Error of pressure in hPa")
    temperature = models.FloatField("Temperature in degrees Celsius")
    temperature_error = models.FloatField("Error of Temperature in degrees Celsius")
    epoch = models.DateTimeField("Observation time")

class LoggerState(models.Model):
    class Action(models.IntegerChoices):
        START = 1
        STOP = 2
    time = models.DateTimeField("Time tag of logging status change")
    # sampling interval, 0 or empty means no sampling is active
    sampling=models.IntegerField("Active sampling interval in seconds")
    action=models.IntegerField("Action which was taken by the sensor logging app",choices=Action.choices)
    pid=models.IntegerField("PID of process which was started")




