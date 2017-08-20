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
    """PONG!"""
    return await killbot.say("Pong!")

@killbot.command(aliases = ['eve_time', 'evetime', 'et'])
async def time():
    """Displays EVE/UTC time."""
    time = datetime.datetime.utcnow()
    return await killbot.say("Current EVE (UTC) Time: " + time.strftime("%H:%M"))


@killbot.command(aliases = ['t'])
async def threat(*, char):
    """ Gets stats for a character from zKill"""
    await kb.getID(char)
    if kb.cid == "0":
        return await killbot.say("Character not found. Please check your spelling and try again.")
    else:
        await kb.get_stats()
    
    return await killbot.say(":alien: "+char+" \n\n :skull_crossbones: "+str(kb.stats[0])+"  :children_crossing:"+str(kb.stats[1])+" :knife: "+str(kb.stats[2])+" :calendar:"+str(kb.stats[3])+"\n\n\n :bookmark: "+kb.kburl)

@killbot.command(aliases = ['pc'])
async def price_check(*, item):
    """ Checks prices for specified items in Jita """
    print(item)
    await market.getID(item)
    if len(market.itemID) == 1:
        return await killbot.say("Item not found. Please check your spelling and try again.")
    else:
        await market.getPrices(market.itemID)

    priceinfo = market.priceinfo
    return await killbot.say(" :chart_with_upwards_trend:  "+ item +"\n\n :regional_indicator_b:     ***Max:*** "+priceinfo[1]+"  ***Min:*** "+priceinfo[0]+"  ***Avg:*** "+priceinfo[2]+" \n :regional_indicator_s:     ***Max:*** "+priceinfo[4]+" ***Min:*** "+priceinfo[3]+" ***Avg:*** "+priceinfo[5]+" \n\n :bookmark: https://eve-central.com/home/quicklook.html?typeid="+market.itemID )

killbot.run(config.BOT_TOKEN)
