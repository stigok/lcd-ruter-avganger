#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.parser import parse as dateparse
from RPi import GPIO
from RPLCD import CharLCD, cursor
import pytz
import json
import fileinput
import sys
import codecs
import time

# Initialise LCD
lcd = CharLCD(pin_rs=26, pin_e=24, pins_data=[22, 18, 16, 12],
              numbering_mode=GPIO.BOARD,
              cols=16, rows=2, dotsize=8,
              auto_linebreaks=True)

# Write to LCD
def writedeparture(line, text):
  print text
  lcd.cursor_pos = (line, 0)
  lcd.write_string(text)

def parsedeparture(departure):
  moncall = departure["MonitoredVehicleJourney"]["MonitoredCall"]
  routeNo = departure["MonitoredVehicleJourney"]["PublishedLineName"]
  routeName = departure["MonitoredVehicleJourney"]["MonitoredCall"]["DestinationDisplay"]
  direction = departure["MonitoredVehicleJourney"]["DirectionName"]
  departureTime = dateparse(moncall["ExpectedDepartureTime"])
  delta = departureTime - datetime.now(pytz.utc)
  minutes = int(delta.total_seconds() / 60)

  lineformat = u'{0:' '>3} {1:' '<9} {2:' '>2}'
  return lineformat.format(routeNo, routeName[0:9], minutes)
  # return routeNo.zfill(3) + ' ' + routeName[0:9] + ' ' + str(minutes)

fp = codecs.open("./avganger.json", "r", "utf-8")
data = json.load(fp)
directionOslo = [dep for dep in data if (dep["MonitoredVehicleJourney"]["DirectionName"] == "1")]

for i in range(0, 1):
    writedeparture(i, parsedeparture(directionOslo[i]))

lcd.close()
