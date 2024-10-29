# sudo apt install python3-pip
# sudo apt install python3-wget
# sudo python3 -m pip install -U discord.py
# sudo python3 -m pip install -U pytz

import os
import sys
import time
import discord
import asyncio
from discord.ext import tasks, commands
from functions import *

intents = discord.Intents.default()
intents.guilds= True
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

serversInfoConfigDir = 'CONFIG_DIRECTORY_PLACEHOLDER'
errorFile = 'ERROR_FILE_PLACEHOLDER'


async def checkConnection():
  await client.wait_until_ready()
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='iRO server'))
  serverStatusFile = 'STATUS_FILE_PLACEHOLDER'
  pingFailureCount = 0

  instructionMessage = 'INSTRUCTION_MESSAGE'

  for filename in os.listdir(serversInfoConfigDir):
    filePath = os.path.join(serversInfoConfigDir, filename)
    if os.path.isfile(filePath):
      statusChannelID = readConfig(filePath, 'STATUS_CHANNELS', 'channel_id')
      if statusChannelID == '':
        continue
      statusChannel = client.get_channel(int(statusChannelID))
      instructionMessageID = readConfig(filePath, 'STATUS_CHANNELS', 'instruction_message_id')
      if instructionMessageID == '':
        instructionMessageID = await statusChannel.send(content=instructionMessage)
        updateConfig(filePath, 'STATUS_CHANNELS', 'instruction_message_id', str(instructionMessageID.id))
      else:
        message = await statusChannel.fetch_message(int(instructionMessageID))
        await message.edit(content=instructionMessage)
      await asyncio.sleep(1)

  try:
    while True:
      warningFlag = False
      isLoginServerDown = False
      isCharServerDown = False
      if readConfig(serverStatusFile, 'LOGIN_SERVER', 'loginServerStatus') != '0':
        isLoginServerDown = True
      if readConfig(serverStatusFile, 'CHAR_SERVER', 'charServerStatus') != '0':
        isCharServerDown = True

      allMapsStatus, warningFlag = serverStatusMessage(isLoginServerDown, isCharServerDown)
      if allMapsStatus is None:
        await asyncio.sleep(5)
        continue
      for filename in os.listdir(serversInfoConfigDir):
        filePath = os.path.join(serversInfoConfigDir, filename)
        if os.path.isfile(filePath):
          statusChannelID = readConfig(filePath, 'STATUS_CHANNELS', 'channel_id')
          if statusChannelID == '':
            continue
          statusChannel = client.get_channel(int(statusChannelID))
          serversInfoMessageID = readConfig(filePath, 'STATUS_CHANNELS', 'servers_info_message_id')
          if serversInfoMessageID == '':
            serversInfoMessageID = await statusChannel.send(content=allMapsStatus)
            updateConfig(filePath, 'STATUS_CHANNELS', 'servers_info_message_id', str(serversInfoMessageID.id))
          else:
            message = await statusChannel.fetch_message(int(serversInfoMessageID))
            await message.edit(content=allMapsStatus)
          await asyncio.sleep(1)

      if isLoginServerDown or isCharServerDown:
        pingFailureCount += 1
        if pingFailureCount == 3:
          pingFailureCount = 0
          for filename in os.listdir(serversInfoConfigDir):
            filePath = os.path.join(serversInfoConfigDir, filename)
            if os.path.isfile(filePath):
              statusChannelID = readConfig(filePath, 'STATUS_CHANNELS', 'channel_id')
              if statusChannelID == '':
                continue
              statusChannel = client.get_channel(int(statusChannelID))
              if statusChannel.name != '🔴iro-status':
                await statusChannel.edit(name='\U0001f534iRO Status', topic='')
              notifyFlag = readConfig(filePath, 'STATUS_CHANNELS', 'notifyflag')
              if notifyFlag == '0':
                updateConfig(filePath, 'STATUS_CHANNELS', 'notifyflag', '1')
                notificationChannelID = readConfig(filePath, 'NOTIFICATION_CHANNELS', 'channel_id')
                if notificationChannelID == '':
                  continue
                notificationChannel = client.get_channel(int(notificationChannelID))
                notifyMessage = "Hey everyone, iRO server is currently down. I will let you all know when the server is back up! \U0001F6D1 \U0001F6A7 \U0001F6D1\n"
                roleID = readConfig(filePath, 'NOTIFICATION_CHANNELS', 'role_id')
                if roleID == '':
                  notifyMessage = f"@here {notifyMessage}"
                else:
                  notifyMessage = f"<@&{roleID}> {notifyMessage}"
                if isLoginServerDown:
                  notifyMessage += ':red_circle: Login Server\n'
                else:
                  notifyMessage += ':green_circle: Login Server\n'
                if isCharServerDown:
                  notifyMessage += ':red_circle: Character Server\n'
                else:
                  notifyMessage += ':green_circle: Character Server\n'

                await notificationChannel.send(notifyMessage)
                await asyncio.sleep(1)

      elif warningFlag:
        for filename in os.listdir(serversInfoConfigDir):
          filePath = os.path.join(serversInfoConfigDir, filename)
          if os.path.isfile(filePath):
            statusChannelID = readConfig(filePath, 'STATUS_CHANNELS', 'channel_id')
            if statusChannelID == '':
              continue
            statusChannel = client.get_channel(int(statusChannelID))
            if statusChannel.name != '⚠️iro-status':
              await statusChannel.edit(name='\U000026a0iRO Status', topic='')
              updateConfig(filePath, 'STATUS_CHANNELS', 'notifyflag', '2')
              await asyncio.sleep(1)

      else:
        pingFailureCount = 0
        for filename in os.listdir(serversInfoConfigDir):
          filePath = os.path.join(serversInfoConfigDir, filename)
          if os.path.isfile(filePath):
            statusChannelID = readConfig(filePath, 'STATUS_CHANNELS', 'channel_id')
            if statusChannelID == '':
              continue
            statusChannel = client.get_channel(int(statusChannelID))
            if statusChannel.name != '🟢iro-status':
              await statusChannel.edit(name='\U0001f7e2iRO Status', topic='')
              notifyFlag = readConfig(filePath, 'STATUS_CHANNELS', 'notifyflag')
              if notifyFlag == '1':
                notificationChannelID = readConfig(filePath, 'NOTIFICATION_CHANNELS', 'channel_id')
                if notificationChannelID == '':
                  continue
                notificationChannel = client.get_channel(int(notificationChannelID))
                notifyMessage = "The server is up!!!\n"
                roleID = readConfig(filePath, 'NOTIFICATION_CHANNELS', 'role_id')
                if roleID == '':
                  notifyMessage = f"@here {notifyMessage}"
                else:
                  notifyMessage = f"<@&{roleID}> {notifyMessage}"
                notificationImage = readConfig(filePath, 'NOTIFICATION_CHANNELS', 'image_file')
                await notificationChannel.send(notifyMessage)
                if notificationImage != '':
                  await notificationChannel.send(file=discord.File(notificationImage))
              updateConfig(filePath, 'STATUS_CHANNELS', 'notifyflag', '0')
            await asyncio.sleep(1)

      await asyncio.sleep(90)

  except Exception as e:
    logError(errorFile, f"An error occurred in checkConnection(): {e}\n")
    await asyncio.sleep(10)
    os.execv(sys.executable, ['/usr/bin/python3'] + sys.argv)


async def callBinaryConvertor():
  try:
    while True:
      currentDayMonth = datetime.now()
      currentDay = currentDayMonth.day
      currentMonth = currentDayMonth.month
      serverDatetime = getServerTimeZone()

      for filename in os.listdir(serversInfoConfigDir):
        filePath = os.path.join(serversInfoConfigDir, filename)
        if os.path.isfile(filePath):
          clabCategoryID = readConfig(filePath, 'CLAB', 'category_id')
          clabChannelID = readConfig(filePath, 'CLAB', 'channel_id')
          if clabCategoryID == '' or clabChannelID == '':
            continue
          cLabCategory = client.get_channel(int(clabCategoryID))
          cLabChannel = client.get_channel(int(clabChannelID))
          if readConfig(filePath, 'CLAB', 'current_day') != str(currentDay):
            updateConfig(filePath, 'CLAB', 'current_day', str(currentDay))
            codeOfTheDay = (currentDay + currentMonth) * 5
            messageTodayCode = "Today\'s code is {}".format(codeOfTheDay)
            cLabMessage = messageTodayCode + '\n' + binaryConvertor(codeOfTheDay, filePath)
            newClabCode = readConfig(filePath, 'CLAB', 'clab_code')
            cLabMessageID = readConfig(filePath, 'CLAB', 'clab_message_id')
            if cLabMessageID == '':
              cLabMessageID = await cLabChannel.send(content=cLabMessage)
              updateConfig(filePath, 'CLAB', 'clab_message_id', str(cLabMessageID.id))
            else:
              message = await cLabChannel.fetch_message(int(cLabMessageID))
              await message.edit(content=cLabMessage)

            firstHalfCode = newClabCode[:4].replace(" ", "")
            secondHalfCode = newClabCode[4:].replace(" ", "")
            newClabCode = firstHalfCode + " " + secondHalfCode
            await cLabChannel.edit(name=newClabCode)
            await cLabCategory.edit(name='Central Lab Code: {}'.format(codeOfTheDay))
          await asyncio.sleep(1)

      await asyncio.sleep(30)

  except Exception as e:
    logError(errorFile, f"An error occurred in callBinaryConvertor(): {e}\n")
    await asyncio.sleep(10)
    os.execv(sys.executable, ['/usr/bin/python3'] + sys.argv)


async def checkPatchUpdate():
  serverStatusJSONFile = 'JSON_FILE_PLACEHOLDER'

  while True:
    data = None
    try:
      for filename in os.listdir(serversInfoConfigDir):
        filePath = os.path.join(serversInfoConfigDir, filename)
        if os.path.isfile(filePath):
          epochTime = int(time.time())
          while True:
            data = getJsonData(serverStatusJSONFile)
            if data is None:
              await asyncio.sleep(5)
              continue
            break
          iroPatchDate = data['iro_patch_status']['last_patch_update']
          wikiPatchDate = data['wiki_patch_status']['last_patch_update']
          iroPatchDate = datetime.fromisoformat(iroPatchDate)
          iroPatchDate = str(iroPatchDate.date())
          wikiPatchDate = datetime.fromisoformat(wikiPatchDate)
          wikiPatchDate = str(wikiPatchDate.date())

          iroPatchHash = str(data['iro_patch_status']['current_patch_hash'])
          wikiPatchHash = str(data['wiki_patch_status']['current_patch_hash'])

          patchChannelID = readConfig(filePath, 'PATCH', 'channel_id')
          if patchChannelID == '':
            continue
          patchChannel = client.get_channel(int(patchChannelID))

          lastiROPatchDate = readConfig(filePath, 'PATCH', 'last_iro_patch_date')
          lastiROPatchHash = readConfig(filePath, 'PATCH', 'last_iro_patch_hash')

          lastWikiPatchDate = readConfig(filePath, 'PATCH', 'last_wiki_patch_date')
          lastWikiPatchHash = readConfig(filePath, 'PATCH', 'last_wiki_patch_hash')

          roleID = readConfig(filePath, 'PATCH', 'role_id')

          if iroPatchDate != lastiROPatchDate or iroPatchHash != lastiROPatchHash:
            updateConfig(filePath, 'PATCH', 'last_iro_patch_date', str(iroPatchDate))
            updateConfig(filePath, 'PATCH', 'last_iro_patch_hash', str(iroPatchHash))
            notifyMessage = "A new iRO patch is now available\n"
            if roleID == '':
              notifyMessage = f"@here {notifyMessage}"
            else:
              notifyMessage = f"<@&{roleID}> {notifyMessage}"
            await patchChannel.send(notifyMessage)

          if wikiPatchDate != lastWikiPatchDate or wikiPatchHash != lastWikiPatchHash:
            updateConfig(filePath, 'PATCH', 'last_wiki_patch_date', str(wikiPatchDate))
            updateConfig(filePath, 'PATCH', 'last_wiki_patch_hash', str(wikiPatchHash))
            notifyMessage = "A new Wiki patch is now available in [iRO Wiki QoL Patcher](<https://irowiki.org/wiki/Clients_and_Patches#iRO_Wiki_QoL_Patcher>)\n"
            if roleID == '':
              notifyMessage = f"@here {notifyMessage}"
            else:
              notifyMessage = f"<@&{roleID}> {notifyMessage}"
            await patchChannel.send(notifyMessage)
          await asyncio.sleep(1)

      await asyncio.sleep(60)

    except Exception as e:
      logError(errorFile, f"An error occurred in checkPatchUpdate(): {e}\n")
      await asyncio.sleep(10)
      os.execv(sys.executable, ['/usr/bin/python3'] + sys.argv)


@client.event
async def on_ready():
  print(f'{client.user} is now running!')
  client.loop.create_task(checkConnection())
  client.loop.create_task(callBinaryConvertor())
  client.loop.create_task(checkPatchUpdate())


@client.event
async def on_message(message):
  if message.author == client.user:
    return


TOKEN='TOKEN_PLACEHOLDER'
client.run(TOKEN)
