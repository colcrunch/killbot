import config

import discord
from discord.ext.commands import Bot

import datetime


import requests

killbot = Bot(command_prefix=config.PREFIX)

@killbot.event
async def on_ready():
    print("Bot online")

@killbot.command()
async def  ping():
    return await killbot.say("Pong!")

@killbot.command(aliases = ['eve_time', 'evetime', 't'])
async def time():
    time = datetime.datetime.utcnow()
    return await killbot.say("Current Eve (UTC) Time: " + time.strftime("%H:%M "))

killbot.run(config.BOT_TOKEN)
