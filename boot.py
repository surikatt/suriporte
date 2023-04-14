from network import WLAN

import pycom
import machine
import time

wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='Projet')
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

machine.main('main.py') #lancement après le boot 