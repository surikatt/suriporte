from pycoproc_1 import Pycoproc
from MFRC630 import MFRC630
import time
import pycom

VALID_CARDS = [[0x9E, 0x56, 0xBF, 0x29]]

py = Pycoproc(Pycoproc.PYSCAN)
nfc = MFRC630(py)

RGB_BRIGHTNESS = 0x8

RGB_RED = (RGB_BRIGHTNESS << 16)
RGB_GREEN = (RGB_BRIGHTNESS << 8)
RGB_BLUE = (RGB_BRIGHTNESS)

def check_uid(uid, len):
    return VALID_CARDS.count(uid[:len])

pycom.heartbeat(False)

nfc.mfrc630_cmd_init()

while True:
    atqa = nfc.mfrc630_iso14443a_WUPA_REQA(nfc.MFRC630_ISO14443_CMD_REQA)

    if (atqa != 0):
        uid = bytearray(10)
        uid_len = nfc.mfrc630_iso14443a_select(uid)

        if (uid_len > 0):
            print("%s" % (nfc.format_block(uid, uid_len)))

            if (check_uid(list(uid), uid_len)) > 0:
                pycom.rgbled(RGB_GREEN)

            else:
                pycom.rgbled(RGB_RED)

    else:
        pycom.rgbled(RGB_BLUE)
    nfc.mfrc630_cmd_reset()
    time.sleep(.5)
    nfc.mfrc630_cmd_init()