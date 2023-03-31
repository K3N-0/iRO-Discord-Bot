import discord
import time
from socket import *

def isServerDown(channel, IP, port_number):
    s = socket(AF_INET, SOCK_STREAM)
    conn = s.connect_ex((IP, port_number))
    s.close()
    return True if conn != 0 else False

def run_discord_bot():
    TOKEN = 'MTA4NjU0MTQ0Nzg2NTU3NzQ5Mw.GtW6uZ.zITHfI1bCxILh1s5j8H-NxzOxN34C30uZFDSj4'
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        channel = client.get_channel(1084917345933328535)
        notified = False

        while True:
            isServer1Down = isServerDown(channel, '128.241.92.36', 6800)
            isServer2Down = isServerDown(channel, '128.241.92.42', 4502)
            isServer3Down = isServerDown(channel, '128.241.92.43', 4500)

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