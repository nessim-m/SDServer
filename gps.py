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
    str = "0"
    gps.update()
    if not gps.has_fix:
 # Try again if we don't have a fix yet.
       str = "36.10"
 #   else:
#	str = "{0:.2}".format(gps.latitude)
    return str
    
def getLongitude():
    str = "0"
    gps.update()
    if not gps.has_fix:
 # Try again if we don't have a fix yet.
       str = "-115.14"
 #   else:
#	str = "{0:.2}".format(gps.longitude)

    return str

def getAltitude():
    str = "0"
    gps.update()
    if not gps.has_fix:
       str = "620.2 m"
 #   else:
  #      str = "{0:.2}".format(gps.altitude_m)

    return str
