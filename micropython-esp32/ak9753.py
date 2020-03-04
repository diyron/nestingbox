
from micropython import const
import utime

AK975X_DEFAULT_ADDRESS = const(0x64) #7-bit unshifted default I2C Address
#Address is changeable via two jumpers on the rear of the PCB.
#Allowed settings are:
#00 (0x64 default)
#01 (0x65)
#10 (0x66)
#11 Not allowed - used for switch mode

I2C_SPEED_STANDARD = const(100000)
I2C_SPEED_FAST = const(400000)

#Register addresses
REG_WIA1       = const(0x00)
REG_WIA2       = const(0x01)
REG_INFO1      = const(0x02)
REG_INFO2      = const(0x03)
REG_INTST      = const(0x04)
REG_ST1        = const(0x05)
REG_IR1L       = const(0x06)
REG_IR1H       = const(0x07)
REG_IR2L       = const(0x08)
REG_IR2H       = const(0x09)
REG_IR3L       = const(0x0A)
REG_IR3H       = const(0x0B)
REG_IR4L       = const(0x0C)
REG_IR4H       = const(0x0D)
REG_TMPL       = const(0x0E)
REG_TMPH       = const(0x0F)
REG_ST2        = const(0x10)
REG_ETH13H_LSB = const(0x11)
REG_ETH13H_MSB = const(0x12)
REG_ETH13L_LSB = const(0x13)
REG_ETH13L_MSB = const(0x14)
REG_ETH24H_LSB = const(0x15)
REG_ETH24H_MSB = const(0x16)
REG_ETH24L_LSB = const(0x17)
REG_ETH24L_MSB = const(0x18)
REG_EHYS13     = const(0x19)
REG_EHYS24     = const(0x1A)
REG_EINTEN     = const(0x1B)
REG_ECNTL1     = const(0x1C)
REG_CNTL2      = const(0x1D)
REG_EKEY       = const(0x50)

## EEPROM
EEPROM_ETH13H_LSB = const(0x51)
EEPROM_ETH13H_MSB = const(0x52)
EEPROM_ETH13L_LSB = const(0x53)
EEPROM_ETH13L_MSB = const(0x54)
EEPROM_ETH24H_LSB = const(0x55)
EEPROM_ETH24H_MSB = const(0x56)
EEPROM_ETH24L_LSB = const(0x57)
EEPROM_ETH24L_MSB = const(0x58)
EEPROM_EHYS13     = const(0x59)
EEPROM_EHYS24     = const(0x5A)
EEPROM_EINTEN     = const(0x5B)
EEPROM_ECNTL1     = const(0x5C)

#Valid sensor modes - Register ECNTL1
AK975X_MODE_STANDBY = const(0b000)
AK975X_MODE_EEPROM_ACCESS =const(0b001)
AK975X_MODE_SINGLE_SHOT = const(0b010)
AK975X_MODE_0 = const(0b100)
AK975X_MODE_1 = const(0b101)
AK975X_MODE_2 = const(0b110)
AK975X_MODE_3 = const(0b111)

#Valid digital filter cutoff frequencies
AK975X_FREQ_0_3HZ = const(0b000)
AK975X_FREQ_0_6HZ = const(0b001)
AK975X_FREQ_1_1HZ = const(0b010)
AK975X_FREQ_2_2HZ = const(0b011)
AK975X_FREQ_4_4HZ = const(0b100)
AK975X_FREQ_8_8HZ = const(0b101)

#Movement
MOVEMENT_NONE        = const(0b0000)
MOVEMENT_FROM_1_TO_3 = const(0b0001)
MOVEMENT_FROM_3_TO_1 = const(0b0010)
MOVEMENT_FROM_2_TO_4 = const(0b0100)
MOVEMENT_FROM_4_TO_2 = const(0b1000)


class AK9753:
    def __init__(self, i2c_sensor):
        self.i2c = i2c_sensor

    def initialize(self):
        utime.sleep_ms(3)
        self.softreset()
        # print(self.getdeviceid())
        if self.get_deviceid() is not 0x13:
            return 0

    def get_companycode(self):   # the code is expected to be 0x48
        return self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_WIA1, 1)

    def get_deviceid(self):      # the ID is expected to be 0x13
        return self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_WIA2, 1)

    def dataready(self):        # returns ST1[0], read ST2 to clear --> dataoverrun()
        tmp = self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_ST1, 1)
        return (tmp & 0x01) == 0x01

    def dataoverrun(self):
        tmp = self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_ST2, 1)
        return (tmp & 0x02) == 0x02

    def get_intst(self):
        return self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_INTST, 1)

    def get_st1(self):
        return self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_ST1, 1)
######################################################################################

    def get_raw_ir1(self):
        tmp = self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_IR1L, 2)
        return (tmp[1] << 8) | tmp[0]

    def get_ir1(self):
        tmp = self.get_raw_ir1()
        return 14286.8 * tmp / 32768

    def get_raw_ir2(self):
        tmp = self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_IR2L, 2)
        return (tmp[1] << 8) | tmp[0]

    def get_ir2(self):
        tmp = self.get_raw_ir2()
        return 14286.8 * tmp / 32768

    def get_raw_ir3(self):
        tmp = self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_IR3L, 2)
        return (tmp[1] << 8) | tmp[0]

    def get_ir3(self):
        tmp = self.get_raw_ir3()
        return 14286.8 * tmp / 32768

    def get_raw_ir4(self):
        tmp = self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_IR4L, 2)
        return (tmp[1] << 8) | tmp[0]

    def get_ir4(self):
        tmp = self.get_raw_ir4()
        return 14286.8 * tmp / 32768
######################################################################################

    def get_raw_temp(self):
        tmp = self.i2c.readfrom_mem(AK975X_DEFAULT_ADDRESS, REG_TMPL, 2)
        return (tmp[1] << 8) | tmp[0]

    def softreset(self):
        self.i2c.writeto_mem(AK975X_DEFAULT_ADDRESS, REG_CNTL2, bytearray(0xFF))





