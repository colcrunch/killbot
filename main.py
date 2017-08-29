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
import asyncio
import sqlite3

killbot = Bot(command_prefix=config.PREFIX)


@killbot.event
async def on_ready():
    print("Bot online")
    print('Logged in as')
    print(killbot.user.name)
    print(killbot.user.id)
    print('------')

#Bot commands go here.
#---------------------------------------------------------------------
#   Ping Command
#   Says "Pong!"
#---------------------------------------------------------------------
@killbot.command()
async def  ping():
    """PONG!"""
    message = "PONG"
    return await killbot.say("Pong!")

#---------------------------------------------------------------------
# Eve Time command
# Returns the current EVE/UTC Time.
#---------------------------------------------------------------------
@killbot.command(aliases = ['eve_time', 'evetime', 'et'])
async def time():
    """Displays EVE/UTC time."""
    time = datetime.datetime.utcnow()
    return await killbot.say("Current EVE (UTC) Time: " + time.strftime("%H:%M"))

#--------------------------------------------------------------------
#   Threat command
#    This command uses kb.py to get the killboard stats of a given character.
#--------------------------------------------------------------------
@killbot.command(aliases = ['t'])
async def threat(*, char: str):
    """ Gets stats for a character from zKill"""
    await kb.getID(char)
    if kb.cid == "0":
        return await killbot.say("Character not found. Please check your spelling and try again.")
    else:
        await kb.get_stats()

    return await killbot.say(":alien: "+char+" \n\n :skull_crossbones: "+str(kb.stats[0])+"  :children_crossing:"+str(kb.stats[1])+" :knife: "+str(kb.stats[2])+" :calendar:"+str(kb.stats[3])+"\n\n\n :bookmark: "+kb.kburl)

@threat.error
async def threat_error(error, ctx):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        return await killbot.say("You must specify a character to look up.")
    else:
        print(error)
        return await killbot.say("Please contact Col Crunch about the following error (make sure to include the exact command that caused it.) \n\n*** Error: ***  "+str(error))

#----------------------------------------------------------------------
# Price Check command
# This command checks jita prices for the given item against the eve-central API
#----------------------------------------------------------------------
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
    plex_msg = ""
    if item == "plex" or item == "PLEX":
        buy_avg = str('{:,}'.format(market.avgs[0]*500))
        sell_avg = str('{:,}'.format(market.avgs[1]*500))
        plexinfo = [buy_avg, sell_avg]
        plex_msg = "**Monthly Sub Cost**  \n ***Sell Avg:*** "+plexinfo[1]+"   ***Buy Avg:*** "+plexinfo[0]+"\n\n "

    return await killbot.say(" :chart_with_upwards_trend:  "+ item +"\n\n "+plex_msg+":regional_indicator_b:     ***Max:*** "+priceinfo[1]+"  ***Min:*** "+priceinfo[0]+"  ***Avg:*** "+priceinfo[2]+" \n :regional_indicator_s:     ***Max:*** "+priceinfo[4]+" ***Min:*** "+priceinfo[3]+" ***Avg:*** "+priceinfo[5]+" \n\n :bookmark: https://eve-central.com/home/quicklook.html?typeid="+market.itemID )

@price_check.error
async def pc_error(error, ctx):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        return await killbot.say("You must specify an item to look up!")
    else:
        print(error)
        return await killbot.say("Please contact Col Crunch about the following error (make sure to include the exact command that caused it.) \n\n *** Error: ***  "+error)

# -----------------------------------------------------------------------
# Status command
# Prints the status of tranquility.
#-----------------------------------------------------------------------
@killbot.command(aliases=['s', 'tq'])
async def status():
    """Prints the status and player count of tranqulilty."""
    headers ={ 'user-agent': "Contact: rhartnett35@gmail.com Project: https://github.com/colcrunch/killbot/ "}
    url = ("https://esi.tech.ccp.is/latest/status/?datasource=tranquility")
    r = requests.get(url, headers=headers)
    status = r.json()
    if 'players' in status:
        return await killbot.say("Tranquility is currently **ONLINE** with "+str('{:,}'.format(status['players']))+" players.")
    else:
        return await killbot.say("Tranquility is currently **OFFLINE** ")

#----------------------------------------------------------------------
# zKill Monitoring.
#----------------------------------------------------------------------
async def watch(chid, watchids):
    await killbot.wait_until_ready()
    counter = 0
    channel = discord.Object(id=chid)
    while not killbot.is_closed:
        counter += 1
        #await killbot.send_message(channel, counter)
        await asyncio.sleep(10)

if config.KILLWATCH_ENABLED == "TRUE":
    print("Watching Corps:" + str(', '.join(config.watchids['corps'])) + " | Alliances:" + str(', '.join(config.watchids['alliances'])) + " | Characters:"+str(', '.join(config.watchids['characters']))+" in " +str(config.KILLWATCH_CHANNEL)+"\n")
    killbot.loop.create_task(watch(config.KILLWATCH_CHANNEL, config.watchids))
#----------------------------------------------------------------------

killbot.run(config.BOT_TOKEN)
