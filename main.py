from mqtt import MQTTClient
from network import WLAN
from pycoproc_1 import Pycoproc
from MFRC630 import MFRC630
from machine import RTC

import pycom
import machine
import time

rtc = RTC()
rtc.ntp_sync("pool.ntp.org",360)
while not rtc.synced():
    time.sleep_ms(50)
print(rtc.now())

py = Pycoproc(Pycoproc.PYSCAN)
nfc = MFRC630(py)

pin = machine.Pin('P9', mode=machine.Pin.IN)
prev_state = None

def sub_cb(topic, msg):
   print(msg)

client = MQTTClient("porte", "172.16.28.48", user="", password="", port=1883)

client.set_callback(sub_cb)
client.connect()

pycom.heartbeat(False)
nfc.mfrc630_cmd_init()

start = time.ticks_ms()

while True:
    state = pin.value()
    temps_actuel = time.ticks_ms()

    if time.ticks_diff(temps_actuel, start) > 60000:
        client.publish(topic="ping:1", msg="ok", qos=1)
        start = temps_actuel

    if state != prev_state:
        #print("L'état de la broche P9 est:", state)
        client.publish(topic="contacteur:1", msg=str(state), qos=1)
        prev_state = state
    
    atqa = nfc.mfrc630_iso14443a_WUPA_REQA(nfc.MFRC630_ISO14443_CMD_REQA)

    if (atqa != 0):
        uid = bytearray(10)
        uid_len = nfc.mfrc630_iso14443a_select(uid)

        if (uid_len > 0):
            #print("ID de la carte:", nfc.format_block(uid, uid_len))
            client.publish(topic="idcarte:1", msg=str(nfc.format_block(uid, uid_len)), qos=1)
        
