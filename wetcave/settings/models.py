from django.db import models
from django.forms import ModelForm

class TankConfig(models.Model):
    deadzone = models.FloatField("Height of the deadzone [m]")
    normalzone = models.FloatField("height of the top of the normal zone (above it will overflow)[m]")
    sounderheight = models.FloatField("Height of the range sensor above the bottom of the tank [m]")
    soundergpiopin = models.IntegerField("Raspberry gpio-pin number of the ultrasounder ranger")
    relay1name = models.CharField("Descriptive Name for the first Relay attached RELAY1",max_length=30)
    relay1gpiopin = models.IntegerField("Raspberry gpio-pin number for controlling the first relay RELAY1")
    relay2name = models.CharField("Descriptive Name for the second Relay attached RELAY2",max_length=30)
    relay2gpiopin = models.IntegerField("Raspberry gpio-pin number for controlling the second relay RELAY2")

class TankLevels(models.Model):
    tankconfig=models.ForeignKey(TankConfig, on_delete=models.CASCADE)
    level = models.FloatField("Height from the bottom of the tank in [m]")
    area = models.FloatField("Horizontal squared area at the indicated height, in [m2]")
    volume = models.FloatField("Accumulated volume in [m3]")

class TankForm(ModelForm):
    class Meta:
        model = TankConfig
        fields = ["deadzone", "normalzone", "sounderheight","soundergpiopin","relay1name","relay1gpiopin","relay2name","relay2gpiopin"]
