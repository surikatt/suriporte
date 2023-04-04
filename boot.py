from network import WLAN
import pycom
import machine
import time
wlan = WLAN(mode=WLAN.STA)
RGB_RED = (RGB_BRIGHTNESS << 16)

wlan.connect(ssid='Projet')
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

pycom.rgbled(RGB_RED)
time.sleep(1)
pycom.rgbled(0x000000)
time.sleep(1)
pycom.rgbled(RGB_RED)
time.sleep(1)
pycom.rgbled(0x000000)

machine.main('main.py') #lancement après le boot 