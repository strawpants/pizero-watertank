from django.db import models
from django.forms import ModelForm,PasswordInput

class TankConfig(models.Model):
    deadzone = models.FloatField("Height of the deadzone [m]")
    normalzone = models.FloatField("height of the top of the normal zone (above it will overflow)[m]")
    sounderheight = models.FloatField("Height of the range sensor above the bottom of the tank [m]",default=1.0)
    # soundergpiopin = models.IntegerField("Raspberry gpio-pin number of the ultrasounder ranger")
    # relay1name = models.CharField("Descriptive Name for the first Relay attached RELAY1",max_length=30)
    # relay1gpiopin = models.IntegerField("Raspberry gpio-pin number for controlling the first relay RELAY1")
    # relay2name = models.CharField("Descriptive Name for the second Relay attached RELAY2",max_length=30)
    # relay2gpiopin = models.IntegerField("Raspberry gpio-pin number for controlling the second relay RELAY2")
    mmtip = models.FloatField("mm/m2 of rain per tipping event of the tipping bucket",default=0.34384)

class TankLevels(models.Model):
    tankconfig=models.ForeignKey(TankConfig, on_delete=models.CASCADE)
    level = models.FloatField("Height from the bottom of the tank in [m]")
    area = models.FloatField("Horizontal squared area at the indicated height, in [m2]")
    volume = models.FloatField("Accumulated volume in [m3]")

class TankForm(ModelForm):
    class Meta:
        model = TankConfig
        fields = ["deadzone", "normalzone", "sounderheight","mmtip"] #,"soundergpiopin","relay1name","relay1gpiopin","relay2name","relay2gpiopin"]

class MQTTConfig(models.Model):
    broker = models.CharField("MQTT broker",max_length=50, default="mqtt.server")
    port = models.IntegerField("MQTT port used",default=8883)
    topic = models.CharField("Root topic to subscribe to",default="wetcave",max_length=30)
    qos = models.IntegerField("QOS level of subscribing messages",default=1)
    clientid = models.CharField("Client id of the subscriber service",default="web",max_length=30)
    pubclientid = models.CharField("Client id of the sensor data publisher",default="tankclient",max_length=30)
    user = models.CharField("MQTT User name",max_length=30,default="mqqtuser")
    password = models.CharField("MQTT Password",max_length=30,default="mqttpw")
    usessl=models.BooleanField("Use SSL for the MQTT connection",default=1)

class MQTTForm(ModelForm):
    class Meta:
        model = MQTTConfig
        fields = ["broker", "port", "topic","qos","clientid","pubclientid","user","password","usessl"]
        widgets = {
            'password': PasswordInput() 
        }
