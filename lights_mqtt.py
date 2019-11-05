import paho.mqtt.client as mqtt
import ssl
import sys
import subprocess
import time
import serial
import randomness
from pynput.keyboard import Key, Controller
import ctypes
from gtts import gTTS 
import winsound 
from pydub import AudioSegment
import http.client, urllib

#Send Push notifications via PushOver, used in the "test" function below
def send_notification(payload):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": "<YOUR TOKEN HERE>",
        "user": "<YOUR USER HERE>",
        "message": payload,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()


#PICK ONE!
#Using Windows? Uncomment this one:
#(Don't forget to figure out which COM port you need)
ser = serial.Serial('COM3', 9600, timeout=1)

#Using Linux? Uncomment this one:
#(Don't forget to figure out which Serial TTY you need)
#ser = serial.Serial('/dev/ttyS3')

#Start the keyboard input stuff.
keyboard = Controller()

#Function to Show the desktop on Windows
def show_desktop():
    keyboard.press(Key.cmd)
    keyboard.press('d')
    keyboard.release('d')
    keyboard.release(Key.cmd)

#Function to Lock the desktop on Windows, using ctypes
def lock_desktop():
    ctypes.windll.user32.LockWorkStation()

#Functions for Light animations:
def lights_fill():
     ser.write(b"mk0\r\n")
     time.sleep(.5)
     ser.write(b"mk1\r\n")
     time.sleep(.5)
     ser.write(b"mk3\r\n")
     time.sleep(.5)
     ser.write(b"mk7\r\n")
     time.sleep(.5)

def lights_fill_reverse():
     ser.write(b"mk0\r\n")
     time.sleep(.5)
     ser.write(b"mk4\r\n")
     time.sleep(.5)
     ser.write(b"mk6\r\n")
     time.sleep(.5)
     ser.write(b"mk7\r\n")
     time.sleep(.5)

def lights_single():
     ser.write(b"mk0\r\n")
     time.sleep(.5)
     ser.write(b"mk1\r\n")
     time.sleep(.5)
     ser.write(b"mk2\r\n")
     time.sleep(.5)
     ser.write(b"mk4\r\n")
     time.sleep(.5)

def lights_single_reverse():
     ser.write(b"mk0\r\n")
     time.sleep(.5)
     ser.write(b"mk4\r\n")
     time.sleep(.5)
     ser.write(b"mk2\r\n")
     time.sleep(.5)
     ser.write(b"mk1\r\n")
     time.sleep(.5)

def lights_flash():
     ser.write(b"mk5\r\n")
     time.sleep(.2)
     ser.write(b"mk2\r\n")
     time.sleep(.2)
     ser.write(b"mk5\r\n")
     time.sleep(.2)
     ser.write(b"mk2\r\n")
     time.sleep(.2)
     ser.write(b"mk5\r\n")
     time.sleep(.2)
     ser.write(b"mk2\r\n")
     time.sleep(.2)
     ser.write(b"mk1\r\n")
     time.sleep(.5)

#Function to use the speech engine on Windows.
def speakit(payload):
    mytext = payload
    language = 'en-ie'
    myobj = gTTS(text=mytext, lang=language, slow=False) 
    myobj.save("welcome.mp3") 
    sound = AudioSegment.from_mp3("welcome.mp3")
    sound.export("myfile.wav", format="wav")
    winsound.PlaySound("myfile.wav", winsound.SND_NOWAIT)

#MQTT Connection:
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    send_notification(client)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#CHANGE THIS TO YOUR TOPIC
    client.subscribe("Light-Tower_test")

#MQTT recieve commands:
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
#Uncomment for eveything to be spoken:    
#    speakit(str(msg.payload.decode("utf-8")))
#IF 'green' turn off the Light tower and then set the light to green
    if str(msg.payload.decode("utf-8")) == "green":
          print(str(msg.payload.decode("utf-8")))
          ser.write(b"mk0\r\n")
          time.sleep(.2)
          ser.write(b"mk1\r\n")
    elif str(msg.payload.decode("utf-8")) == "red":
          print(str(msg.payload.decode("utf-8")))
          ser.write(b"mk0\r\n")
          time.sleep(.2)
          ser.write(b"mk4\r\n")
    elif str(msg.payload.decode("utf-8")) == "yellow":
          print(str(msg.payload.decode("utf-8")))
          ser.write(b"mk0\r\n")
          time.sleep(.2)
          ser.write(b"mk2\r\n")
#IF 'GREEN' set the light to green (don't turn everything off first, just go green)
    elif str(msg.payload.decode("utf-8")) == "GREEN":
          print(str(msg.payload.decode("utf-8")))
          ser.write(b"mk1\r\n")
    elif str(msg.payload.decode("utf-8")) == "YELLOW":
          print(str(msg.payload.decode("utf-8")))
          ser.write(b"mk2\r\n")
    elif str(msg.payload.decode("utf-8")) == "RED":
          print(str(msg.payload.decode("utf-8")))
          ser.write(b"mk4\r\n")
#IF 'fill' run the fill animation.
    elif str(msg.payload.decode("utf-8")) == "fill":
          print(str(msg.payload.decode("utf-8")))
          lights_fill()
    elif str(msg.payload.decode("utf-8")) == "RFILL":
          print(str(msg.payload.decode("utf-8")))
          lights_fill_reverse()
    elif str(msg.payload.decode("utf-8")) == "single":
          print(str(msg.payload.decode("utf-8")))
          lights_single()
    elif str(msg.payload.decode("utf-8")) == "RSING":
          print(str(msg.payload.decode("utf-8")))
          lights_single_reverse()
#IF 'off' turn off all the lights
    elif str(msg.payload.decode("utf-8")) == "off":
          print(str(msg.payload.decode("utf-8")))
          ser.write(b"mk0\r\n")
#Another animation
    elif str(msg.payload.decode("utf-8")) == "flash":
          print(str(msg.payload.decode("utf-8")))
          lights_flash()
#IF 'random' run the external function to create a random number, then pull a list of "Shower thoughts" from Reddit, and use the random number to select which 'thought' to post back into the MQTT channel.
    elif str(msg.payload.decode("utf-8")) == "random":
          print(str(msg.payload.decode("utf-8")))
          randomness.randomizer_func()
#IF 'desktop' call the function to show the desktop WINDOWS ONLY
    elif str(msg.payload.decode("utf-8")) == "desktop":
          show_desktop()
#IF 'lock my desktop' call the function to... you know
    elif str(msg.payload.decode("utf-8")) == "lock my desktop":
          lock_desktop()
#IF 'test' do some stuff by calling that random external function.
    elif str(msg.payload.decode("utf-8")) == "test":
          randomness.test_reply()
          speakit("Hello World")
          send_notification(str(msg.payload.decode("utf-8")))




#MQTT CONNET STUFF
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set("mosquitto.org.crt", tls_version=ssl.PROTOCOL_TLSv1_2)


#PUT YOUR MQTT SERVER INFO HERE, or use the test server.
client.connect("test.mosquitto.org", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
