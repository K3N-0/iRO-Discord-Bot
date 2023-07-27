import os
import discord
import asyncio
from socket import *
from discord.ext import tasks, commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def isServerDown(IP, port_number):
  s = socket(AF_INET, SOCK_STREAM)
  s.settimeout(5)
  conn = s.connect_ex((IP, port_number))
  s.close()
  return True if conn != 0 else False

def readFile(notifiedFilename):
  f = open(notifiedFilename, "r")
  ret = f.readline()
  f.close()
  return ret

def writeFile(notifiedFilename, data):
  f = open(notifiedFilename, "w")
  f.write(data)
  f.close()

async def checkConnection():
  await client.wait_until_ready()
  generalChannel = client.get_channel(CHANNEL_ID_1)
  statusChannel = client.get_channel(CHANNEL_ID_2)
  notifiedFilename = "notified.txt"
  pingFailureCount = 0
  await statusChannel.edit(name='iRO Status: \U0001F7E2', topic='\U0001F600')

  # await generalChannel.send('Hey @here I\'m new here and my job is to monitor the server for you. Have a nice day!!!')
  # await generalChannel.send(file=discord.File('images/gxDance.gif'))

  while True:
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='iRO server'))
    isLoginServerDown = isServerDown('LOGIN_SERVER_IP', 6800)  # Login server
    isServer1Down = isServerDown('SERVER_1_IP', 4502)  # Character server 1
    isServer2Down = isServerDown('SERVER_2_IP', 4500)  # Character server 2

    if isLoginServerDown or isServer1Down or isServer2Down:
      pingFailureCount += 1
      if pingFailureCount == 2:
        pingFailureCount = 0
        await statusChannel.edit(name='iRO Status: \U0001F534', topic='\U0001F634')
        if readFile(notifiedFilename) == "0":
          writeFile(notifiedFilename, "1")
          await generalChannel.send('@here Hey everyone, the iRO server is currently down. I will let you all know when the server is back up! \U0001F6D1 \U0001F6A7 \U0001F6D1')
          if isLoginServerDown:
            await generalChannel.send('Login Server -> ' + '\U0001F534')
          else:
            await generalChannel.send('Login Server -> ' + '\U0001F7E2')
          if isServer1Down:
            await generalChannel.send('Character Server 1 -> ' + '\U0001F534')
          else:
            await generalChannel.send('Character Server 1 -> ' + '\U0001F7E2')
          if isServer2Down:
            await generalChannel.send('Character Server 2 -> ' + '\U0001F534')
          else:
            await generalChannel.send('Character Server 2 -> ' + '\U0001F7E2')

      await asyncio.sleep(30)

    else:
      if readFile(notifiedFilename) == "1":
        await generalChannel.send('Hey @everyone, the server is back up!!! \U0001F7E2 \U0001F7E2 \U0001F7E2')
        await generalChannel.send(file=discord.File('images/Kenfra_server_up.gif'))
        await statusChannel.edit(name='iRO Status: \U0001F7E2', topic='\U0001F600')
        writeFile(notifiedFilename, "0")

      await asyncio.sleep(60)


@client.event
async def on_ready():
  print(f'{client.user} is now running!')
  client.loop.create_task(checkConnection())


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$botStatus'):
    await message.channel.send('I am still alive!')


keep_alive()
token = os.environ.get('YOUR_TOKEN')
client.run(token)
