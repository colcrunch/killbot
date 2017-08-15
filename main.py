import os
import config
import discord
import datetime
from discord.ext.commands import Bot

import requests

killbot = Bot(command_prefix=config.PREFIX)

@killbot.event
async def on_read():
    print("Bot online")

@killbot.command()
async def  ping():
    return await killbot.say("Pong!")

@killbot.command()
async def time():
    return await datetime.datetime.utcnow("HH:mm")

killbot.run(config.BOT_TOKEN)
