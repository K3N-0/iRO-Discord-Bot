# sudo apt install python3-pip
# sudo apt install python3-wget
# sudo python3 -m pip install -U discord.py
# sudo python3 -m pip install -U pytz

import os
import wget
import json
import pytz
from socket import *
from configparser import ConfigParser
from datetime import datetime, time, timedelta


def isServerDown(IP, port_number):
  s = socket(AF_INET, SOCK_STREAM)
  s.settimeout(5)
  conn = s.connect_ex((IP, port_number))
  s.close()
  return True if conn != 0 else False

def readNotifyConfig(input_config):
  configObj = ConfigParser()
  configObj.read(input_config)
  notifyFlag = configObj['NOTIFY_FLAG']
  return notifyFlag['notifyFlag']

def updateNotifyConfig(input_config, flag):
  configObj = ConfigParser()
  configObj.read(input_config)
  newNotifyFlag = configObj['NOTIFY_FLAG']
  newNotifyFlag['notifyFlag'] = flag
  with open(input_config, 'w') as conf:
    configObj.write(conf)

def serverStatusMessage(serverStatusFile, isLoginServerDown, isCharServerDown, warningFlag=False):
  if os.path.exists(serverStatusFile):
    os.remove(serverStatusFile)

  wget.download('https://db.irowiki.org/server_status.json', out=serverStatusFile, bar=False)
  jsonFile = open(serverStatusFile,)
  data = json.load(jsonFile)
  jsonFile.close()

  dateNow = data['last_update']
  dateParser = dateNow.split('-')
  year = dateParser[0]
  month = dateParser[1]

  dateParser_1 = dateParser[2].split('T')
  date = dateParser_1[0]

  dateParser_2 = dateParser_1[1].split(':')
  hour = dateParser_2[0]
  minute = dateParser_2[1]
  second = dateParser_2[2]

  utcTimezone = datetime(int(year), int(month), int(date), int(hour), int(minute), int(second), tzinfo=pytz.utc)
  serverTimezone = pytz.timezone('America/Los_Angeles')
  serverDatetime = utcTimezone.astimezone(serverTimezone)
  allMapsStatus = '## List of Server Status(Live)\n### Last update(server timezone): ***{}***\n'.format(serverDatetime.strftime('%Y-%m-%d %H:%M:%S'))

  for service in data['services']['HTTP']:
    if service['status'] == 'online':
      allMapsStatus += '\U0001F7E2 ' + service['name'] + '\n'
    else:
      allMapsStatus += '\U0001F534 ' + service['name'] + '\n'
      warningFlag = True

  for service in data['services']['FTP']:
    if service['status'] == 'online':
      allMapsStatus += '\U0001F7E2 ' + service['name'] + '\n\n'
    else:
      allMapsStatus += '\U0001F534 ' + service['name'] + '\n\n'
      warningFlag = True

  if isLoginServerDown:
    allMapsStatus += '\U0001F534 Login server' + '\n'
  else:
    allMapsStatus += '\U0001F7E2 Login server' + '\n'

  if isCharServerDown:
    allMapsStatus += '\U0001F534 Character server' + '\n\n'
  else:
    allMapsStatus += '\U0001F7E2 Character server' + '\n\n'

  for map in data['map']['chaos']:
    if map['status'] == 'online':
      allMapsStatus += '\U0001F7E2 ' + map['name'] + '\n'
    else:
      allMapsStatus += '\U0001F534 ' + map['name'] + '\n'
      warningFlag = True

  return allMapsStatus
