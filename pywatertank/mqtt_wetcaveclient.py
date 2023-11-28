import paho.mqtt.client as mqtt
import ssl
clientid="wetcave"
version = '3' # or '3' 
mytransport = 'tcp' # or 'tcp'
broker='mqtt.wobbly.earth'
myport=1883
topic="debug"

if version == '5':
    client = mqtt.Client(client_id=clientid,
                         transport=mytransport,
                         protocol=mqtt.MQTTv5)
if version == '3':
    client = mqtt.Client(client_id=clientid,
                         transport=mytransport,
                         protocol=mqtt.MQTTv311,
                         clean_session=True)
user='buzz'
pw='BD5TZczmkrhofrTVafAZ'
client.username_pw_set(user,pw)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

# client.tls_set(certfile=None,
               # keyfile=None,
               # cert_reqs=ssl.CERT_REQUIRED)

client.connect(broker,port=myport,keepalive=60);


# post a message
res=client.publish(topic,f"This is a test message")

if res[0] == 0:
    print("succeeded in publishing message")

