# sudo apt install python3-pip
# sudo apt install python3-wget
# sudo python3 -m pip install -U discord.py
# sudo python3 -m pip install -U pytz

import os
import sys
import discord
import asyncio
from discord.ext import tasks, commands
from functions import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

async def checkConnection():
  await client.wait_until_ready()
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='iRO server'))
  generalChannel = client.get_channel("GENERAL_CHANNEL_ID_PLACEHOLDER")
  statusChannel = client.get_channel("STATUS_CHANNEL_ID_PLACEHOLDER")
  notifyConfig = 'NOTIFY_FILE_PATH'
  serverStatusFile = 'JSON_FILE_PATH'
  pingFailureCount = 0

  # await generalChannel.send('Hey @here I\'m new here and my job is to monitor the server for you. Have a nice day!!!')
  # await generalChannel.send(file=discord.File('images/gxDance.gif'))

  try:
    while True:
      warningFlag = False
      isLoginServerDown = isServerDown('IP_ADDR_PLACEHOLDER', PORT_NUM)  # Login server
      isCharServerDown = isServerDown('IP_ADDR_PLACEHOLDER', PORT_NUM)   # Character server
      allMapsStatus = serverStatusMessage(serverStatusFile, isLoginServerDown, isCharServerDown, warningFlag)
  #    await statusChannel.send(allMapsStatus)
      message = await statusChannel.fetch_message(MESSAGE_ID)
      await message.edit(content=allMapsStatus)

      if isLoginServerDown or isCharServerDown:
        pingFailureCount += 1
        if pingFailureCount == 3:
          pingFailureCount = 0
          await statusChannel.edit(name='\U0001F534iRO Status', topic='\U0001F634')
          notifyFlag = readNotifyConfig(notifyConfig)
          if notifyFlag == '0':
            updateNotifyConfig(notifyConfig, '1')
            notifyMessage = '<@&NOTIFY_ROLE_ID> iRO server is currently down. I will let you all know when the server is back up! \U0001F6D1 \U0001F6A7 \U0001F6D1\n'
            if isLoginServerDown:
              notifyMessage += 'Login Server -> \U0001F534\n'
            else:
              notifyMessage += 'Login Server -> \U0001F7E2\n'
            if isCharServerDown:
              notifyMessage += 'Character Server -> \U0001F534\n'
            else:
              notifyMessage += 'Character Server -> \U0001F7E2\n'

            await generalChannel.send(notifyMessage)

        await asyncio.sleep(90)

      else:
        pingFailureCount = 0
        if warningFlag:
          await statusChannel.edit(name='\U0001F7E0iRO Status', topic='\U0001F912')
        else:
          await statusChannel.edit(name='\U0001F7E2iRO Status', topic='\U0001F600')
        notifyFlag = readNotifyConfig(notifyConfig)
        if notifyFlag == '1':
          await generalChannel.send('<@&NOTIFY_ROLE_ID> The server is up!!! \U0001F7E2 \U0001F7E2 \U0001F7E2')
          await generalChannel.send(file=discord.File('/home/ken/liveServers/juno/images/Kenfra_server_up.gif'))
          updateNotifyConfig(notifyConfig, '0')

        await asyncio.sleep(60)

  except Exception as error:
    os.execv(sys.executable, ['/usr/bin/python3'] + sys.argv)


@client.event
async def on_ready():
  print(f'{client.user} is now running!')
  client.loop.create_task(checkConnection())


@client.event
async def on_message(message):
  if message.author == client.user:
    return

#  if message.content.startswith('$botStatus'):
#    await message.channel.send('I am still alive!')

  cLabChannelID = 1187498424514400298
  if message.channel.id != cLabChannelID:
    return

  if message.content.startswith('$'):
    bit_length = 8
    decimal_number = message.content[1:]
    if decimal_number.isdigit():
      decimal_number = int(decimal_number)
    else:
      return

    # Convert decimal to binary with leading zeros
    binary_number = format(decimal_number, '0' + str(bit_length) + 'b')

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

    if len(formatted_binary) == 9:
      myStringResult = "```fix\n{res}\n```".format(res = formatted_binary + '\n' + index_positions)
      cLabChannel = client.get_channel(cLabChannelID)
      await cLabChannel.send(myStringResult)


@client.event
async def on_member_join(member):
  await client.get_channel(WELCOME_CHANNEL_ID).send(f"Hello {member.mention}, welcome to Juno Citizen IRO server! Before you can get access to all channels, please fill out your information in LINK_TO_INTRO_CHANNEL using the following template:\n```Name: (What do you like people to call you)\nIGN: (In Game Name)\nCharacter: (Job/Classes you play)\nLocation: (Your current country staying at)\nWho invited you: (Who or how you get to know us)```\nClick the green circle in LINK_TO_STATUS_CHANNEL if you want to get notification of when iRO server is up/down\nEnjoy your stay!!!")


TOKEN='SECRET_TOKEN'
client.run(TOKEN)
