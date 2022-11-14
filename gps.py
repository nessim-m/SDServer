import time
import board
import busio
import adafruit_gps
import serial

i2c = busio.I2C(board.SCL, board.SDA)

gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

gps.send_command(b"PMTK220,1000")

def getLatitude():
    gps.update()
    return gps.latitude()
    
def getLongitude():
    gps.update()
    return gps.longitude()
