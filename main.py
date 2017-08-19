#Import bot scripts
import config
import kb
import market

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

@killbot.command(aliases = ['eve_time', 'evetime', 'et'])
async def time():
    time = datetime.datetime.utcnow()
    return await killbot.say("Current EVE (UTC) Time: " + time.strftime("%H:%M"))


@killbot.command(aliases = ['t'])
async def threat(*, char):
    print(char)
    await kb.getID(char)
    if kb.cid == "0":
        return await killbot.say("Character not found. Please check your spelling and try again.")
    else:
        await kb.get_stats()

    return await killbot.say(":alien: "+char+" \n\n :skull_crossbones: "+str(kb.stats[0])+"  :children_crossing:"+str(kb.stats[1])+" :knife: "+str(kb.stats[2])+" :calendar:"+str(kb.stats[3])+"\n\n\n :bookmark: "+kb.kburl)

killbot.run(config.BOT_TOKEN)
