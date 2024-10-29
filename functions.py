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
from datetime import datetime, timedelta


def getServerTimeZone():
  currentDatetime = datetime.now()
  return currentDatetime.strftime('%Y-%m-%d %H:%M:%S')

def logError(error_file, error_message):
  with open(error_file, "a") as file:
    currentTime = getServerTimeZone()
    file.write(f"{currentTime} --- {error_message}")

def readWoEConfig(input_config):
  configObj = ConfigParser()
  configObj.read(input_config)
  remindFlag = configObj['REMIND_FLAG']
  scheduleDate = configObj['SCHEDULE_DATE']
  return remindFlag['remindFlag'], scheduleDate['scheduleDate']

def updateWoEConfig(input_config, flag, new_schedule_date):
  configObj = ConfigParser()
  configObj.read(input_config)
  newReminderFlag = configObj['REMIND_FLAG']
  newReminderFlag['remindFlag'] = flag

  if len(new_schedule_date) > 0:
    newScheduleDate = configObj['SCHEDULE_DATE']
    newScheduleDate['scheduleDate'] = new_schedule_date

  with open(input_config, 'w') as conf:
    configObj.write(conf)

def readConfig(config_file, section_name, subsection):
  configObj = ConfigParser()
  configObj.read(config_file)
  notifyFlag = configObj[section_name]
  return notifyFlag[subsection]

def updateConfig(config_file, section_name, subsection, flag):
  configObj = ConfigParser()
  configObj.read(config_file)
  newNotifyFlag = configObj[section_name]
  newNotifyFlag[subsection] = flag
  with open(config_file, 'w') as conf:
    configObj.write(conf)

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

def getJsonData(filename):
  with open(filename, 'r') as file:
    fileData = file.read().strip()
    if not fileData:
      return None
    return json.loads(fileData)

def serverStatusMessage(isLoginServerDown, isCharServerDown):
  allMapsStatus = None
  warningFlag = False
  serverStatusFile = '/home/ken/liveServers/server_status.json'
  data = getJsonData(serverStatusFile)
  if data is None:
    return allMapsStatus, warningFlag

  allMapsStatus = '### Last update(server timezone): ***{}***\n'.format(getServerTimeZone())

  for service in data['services']['HTTP']:
    if service['status'] == 'online':
      allMapsStatus += ':white_check_mark: ' + service['name'] + '\n'
    else:
      allMapsStatus += ':small_red_triangle_down: ' + service['name'] + '\n'
      warningFlag = True

  if isLoginServerDown:
    allMapsStatus += '\n:small_red_triangle_down: Login server' + '\n'
  else:
    allMapsStatus += '\n:white_check_mark: Login server' + '\n'

  if isCharServerDown:
    allMapsStatus += ':small_red_triangle_down: Character server' + '\n\n'
  else:
    allMapsStatus += ':white_check_mark: Character server' + '\n\n'

  for map in data['map']['chaos']:
    if map['status'] == 'online':
      allMapsStatus += ':white_check_mark: ' + map['name'] + '\n'
    else:
      allMapsStatus += ':small_red_triangle_down: ' + map['name'] + '\n'
      warningFlag = True

  return allMapsStatus, warningFlag

def binaryConvertor(decimal_number, clab_config):
  # Convert decimal to binary with leading zeros
  binary_number = format(decimal_number, '0' + str(8) + 'b')

  # Insert a space between the fourth and fifth positions
  formatted_binary = binary_number[:4] + ' ' + binary_number[4:]

  # Create a string with the index positions for '1's in the binary representation
  index_positions = ''
  i = 1
  for bit in formatted_binary:
    if bit == '1':
      index_positions += str(i)
    else:
      index_positions += ' '
    i += 1
    if bit == ' ':
      i -= 1

  updateConfig(clab_config, 'CLAB', 'clab_code', index_positions)
  myStringResult = "```fix\n{res}\n```".format(res = formatted_binary + '\n' + index_positions)
  return myStringResult
