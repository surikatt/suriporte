from mqtt import MQTTClient
# from mqtt import MQTTClient_lib as MQTTClient
from network import WLAN
import machine
import time
from pycoproc_1 import Pycoproc
from MFRC630 import MFRC630
import pycom

VALID_CARDS = [[0x9E, 0x56, 0xBF, 0x29]]

py = Pycoproc(Pycoproc.PYSCAN)
nfc = MFRC630(py)

RGB_BRIGHTNESS = 0x8

RGB_RED = (RGB_BRIGHTNESS << 16)
RGB_GREEN = (RGB_BRIGHTNESS << 8)
RGB_BLUE = (RGB_BRIGHTNESS)

pin = machine.Pin('P9', mode=machine.Pin.IN)
prev_state = None

def check_uid(uid, len):
    return VALID_CARDS.count(uid[:len])

def sub_cb(topic, msg):
   print(msg)

client = MQTTClient("porte", "172.16.28.48", user="", password="", port=1883)

client.set_callback(sub_cb)
client.connect()

pycom.heartbeat(False)
nfc.mfrc630_cmd_init()

while True:
    state = pin.value()
    if state != prev_state:
        #print("L'état de la broche P9 est:", state)
        client.publish(topic="contacteur:1", msg=str(state))
        prev_state = state
    
    atqa = nfc.mfrc630_iso14443a_WUPA_REQA(nfc.MFRC630_ISO14443_CMD_REQA)

    if (atqa != 0):
        uid = bytearray(10)
        uid_len = nfc.mfrc630_iso14443a_select(uid)

        if (uid_len > 0):
            #print("ID de la carte:", nfc.format_block(uid, uid_len))
            client.publish(topic="idcarte:1*", msg=str(nfc.format_block(uid, uid_len)))

            if (check_uid(list(uid), uid_len)) > 0:
                pycom.rgbled(RGB_GREEN)

            else:
                pycom.rgbled(RGB_RED)

    else:
        pycom.rgbled(RGB_BLUE)
    nfc.mfrc630_cmd_reset()
    time.sleep(.5)
    nfc.mfrc630_cmd_init()
    #client.check_msg()
    time.sleep(0.1)
