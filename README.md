# MQTT-Light-Tower
Controls for Serial Industrial Light Towers using MQTT and Python

This is a hodge-podge of exploration test scripts that I've consolidated into one script that does a few things.
It started as a way to control an industrial light tower over serial, but I slowly added more things like MQTT, text to speech, emulating keyboard inputs and web scraping.

I'm not sure if this is a comprehensive list of packages I've installed via PIP, but here's what I think is needed for this project:
pyserial
paho-mqtt
gTTS
playsound
pydub
pynput
requests
urllib3

The current configuration runs on Windows 10, so you'll need to install Python3 for Windows. If you're on linux, you'll lose the Text to Speech and keyboard inputs and need to change the serial path to the /dev/tty and comment out the Windows COM, as it's configured now. I've only tested the linux specific code using "Windows Subsystem for Linux" (WSL).

You'll need your serial device connected to the computer running the lights_mqtt.py script and you'll need to know which serial port/tty to connect to, my computer shows it as COM3 or ttyS3 depending on if I'm using the CMD window or the Ubuntu WSL terminal.

When you start the script, just type in:  python3 lights_mqtt.py  and it should connect to the test.mosquitto.org server. You can host your own mosquitto server and just type in it's address instead of test.mosquitto.org.

With the script running, you can open the html file new_lights.html and it will also connect to the test.mosquitto.org server over websockets. When you press the buttons, you should see the output in the script window and in the html text window.

---more later---
