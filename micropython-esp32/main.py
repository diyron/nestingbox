

from machine import I2C, Pin
from ak9753 import AK9753

i2c = I2C(scl=Pin(22), sda=Pin(21))
sensor = AK9753(i2c_sensor=i2c)
sensor.initialize()

