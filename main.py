#Import bot scripts
import config
import kb

#Import discord python library
import discord
from discord.ext.commands import Bot

#Import other libraries needed
import datetime
import requests

killbot = Bot(command_prefix=config.PREFIX)


@killbot.event
async def on_ready():
    print("Bot online")

#Bot commands go here.
@killbot.command()
async def  ping():
    return await killbot.say("Pong!")

@killbot.command(aliases = ['eve_time', 'evetime', 't'])
async def time():
    time = datetime.datetime.utcnow()
    return await killbot.say("Current EVE (UTC) Time: " + time.strftime("%H:%M "))


@killbot.command()
async def threat(*args):
    print(args)
    char = '%20'.join(args)
    await kb.getID(char)
    return await killbot.say("Feature in development. "+ char + "\n" + kb.URL)

killbot.run(config.BOT_TOKEN)
