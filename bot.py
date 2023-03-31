import discord
import time
from socket import *

def isServerDown(channel, IP, port_number):
    s = socket(AF_INET, SOCK_STREAM)
    conn = s.connect_ex((IP, port_number))
    s.close()
    return True if conn != 0 else False

def run_discord_bot():
    # Never shared YOUR_TOKEN with someone you do not know
    TOKEN = 'YOUR_TOKEN'
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        # To obtain your channel id, turn on developer mode on your discord. Then right-click on you channel tab and click Copy ID.
        channel = client.get_channel(YOUR_CHANNEL_ID)
        notified = False

        while True:
            isServer1Down = isServerDown(channel, 'IP1', PORT1)
            isServer2Down = isServerDown(channel, 'IP2', PORT2)
            isServer3Down = isServerDown(channel, 'IP3', PORT3)

            if(isServer1Down or isServer2Down or isServer3Down):
                if(not notified):
                    await channel.send('Hey @everyone Server is down')
                    notified = True

            elif(not isServer1Down and not isServer2Down and not isServer3Down):
                if(notified):
                    await channel.send('Hey @everyone Server is up')
                    notified = False

            time.sleep(300)

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)