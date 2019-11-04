import random
import paho.mqtt.client as mqtt
import ssl
import sys
import time
import requests
import json

def sendingit(payload):
        mybroker_address="test.mosquitto.org"
        myclient = mqtt.Client("randomthoughts")
#        myclient.tls_set("/etc/ssl/certs/ca-certificates.crt"
        myclient.tls_set("mosquitto.org.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
#        myclient.tls_insecure_set(True)
        myclient.connect(mybroker_address, 8883, 60)
        myclient.publish("test", (payload))
#        print((payload))


def randomizer_func():
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        rando = random.randint(13,30)
        randz = random.randint(0,12)
        zero = rando-randz-1
        one = rando-2
        two = rando-3
#            print(rando)
#            print(randz)
#            print(zero)
        url = "https://www.reddit.com/r/Showerthoughts/top/.json?t=hour&limit=31"
        page = requests.get(url=url, headers=headers, verify=True)
        jsondata=page.json()
        message0 = jsondata['data']['children'][(zero)]['data']['title']
        payload = message0 +"\n"
        sendingit(payload)

def test_reply():
        payload = "The script is running\n"
        sendingit(payload)

if __name__=='__main__':
        randomizer_func()
