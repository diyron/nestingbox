print("hello world")


data = {"tin": 0,
        "hin": 0,
        "tnest": 0,
        "tout": 0,
        "hout": 0,
        "pout": 0,

        "ired": {
                "ir1": 0,
                "ir2": 0,
                "ir3": 0,
                "ir4": 0,
                "tir": 0,
                },

        "vbat": 0,
        "lon": 0,
        "lat": 0,
        "lorasf": "",
        "tstamp": ""

        }



######################################################################
# LORA

import utime
import ujson
from libs.ulora import uLoRa, TTN

# Refer to device pinout / schematics diagrams for pin details

LORA_CS = const(18)
LORA_SCK = const(5)
LORA_MOSI = const(27)
LORA_MISO = const(19)
LORA_IRQ = const(26)
LORA_RST = const(14)

LORA_DATARATE = "SF9BW125"  # Choose from several available
FPORT = 1

# From TTN console for device
DEVADDR = bytearray([0x26, 0x01, 0x17, 0xE9])
NWSKEY = bytearray([0x00, 0x44, 0x63, 0xB9, 0xBA, 0xDF, 0x11, 0xDB, 0xDF, 0xF2, 0xA8, 0x77, 0x86, 0xF2, 0x8B, 0x92])
APPSKEY = bytearray([0xF3, 0x18, 0x35, 0xAC, 0xA2, 0x57, 0xC3, 0x9B, 0xEF, 0x26, 0xEE, 0x3A, 0x5D, 0x77, 0xC0, 0x95])

TTN_CONFIG = TTN(DEVADDR, NWSKEY, APPSKEY, country="EU")

lora = uLoRa(
    cs=LORA_CS,
    sck=LORA_SCK,
    mosi=LORA_MOSI,
    miso=LORA_MISO,
    irq=LORA_IRQ,
    rst=LORA_RST,
    ttn_config=TTN_CONFIG,
    datarate=LORA_DATARATE,
    fport=FPORT
)

testdata = {"key1": "Hello",
            "key2": "World!"}

data = ujson.dumps(testdata)  # dictionary to json

buf = bytearray(data, 'utf-8')
print(buf)
print("send data")
# ...Then send data as bytearray

lora.send_data(buf, len(buf), lora.frame_counter)


######################################################################
# onewire

from machine import Pin
import onewire

ow = onewire.OneWire(Pin(12)) # create a OneWire bus on GPIO12

import time, ds18x20

ds = ds18x20.DS18X20(ow)
roms = ds.scan()
for rom in roms:
    print(rom)
ds.convert_temp()
time.sleep_ms(750)
for rom in roms:
    print(ds.read_temp(rom))

