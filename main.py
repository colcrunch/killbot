#Import bot scripts
import config
import kb
import market

#Import discord python library
import discord
from discord.ext.commands import Bot

#Import other libraries needed
import datetime
import asyncio
import aiohttp
import sqlite3
import re

killbot = Bot(command_prefix=config.PREFIX)

@killbot.event
async def on_ready():
    print("Bot online")
    print('------')
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
    if market.itemID == "None":
        return await killbot.say("Item not found. Please check your spelling and try again.")
    else:
        await market.getPrices(market.itemID)

    priceinfo = market.priceinfo
    plex_msg = ""
    if item.lower() == "plex":
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
    async with aiohttp.ClientSession() as session:
        status = await kb.fetch(session, "https://esi.tech.ccp.is/latest/status/?datasource=tranquility")
    if 'players' in status:
        return await killbot.say("Tranquility is currently **ONLINE** with "+str('{:,}'.format(status['players']))+" players.")
    else:
        return await killbot.say("Tranquility is currently **OFFLINE** ")
#----------------------------------------------------------------------
# Github command
# Hidden, but will bring up github info
#----------------------------------------------------------------------
@killbot.command(aliases=['gh'], hidden='true')
async def github():
    """Prints github repo link"""
    return await killbot.say("https://github.com/colcrunch/killbot")

#----------------------------------------------------------------------
# zKill Monitoring.
#----------------------------------------------------------------------
async def watch_redisq(chid, watchids):
    wids = config.watchids
    await killbot.wait_until_ready()
    counter = 0
    channel = discord.Object(id=chid)
    while not killbot.is_closed:
        counter += 1
        url = "https://redisq.zkillboard.com/listen.php"
        async with aiohttp.ClientSession() as session:
            kills = await kb.fetch(session, url)
        attackers = kills['package']['killmail']['attackers']
        killID= str(kills['package']['killID'])
        victim = kills['package']['killmail']['victim']
        message = "https://zkillboard.com/kill/"+killID+"/"
        vic = 0
        print(killID)
        #Are we tracking any of the groups that are the attackers?
        for attacker in attackers:
            if 'alliance' in attacker and attacker['alliance']['id_str'] in wids['alliances']:
                print("Watching Attacker in "+killID)
                await killbot.send_message(channel, message)
                break
            elif 'corporation' in attacker and attacker['corporation']['id_str'] in wids['corps']:
                print("Watching Attacker in "+killID)
                await killbot.send_message(channel, message)
                break
            elif 'character' in attacker and attacker['character']['id_str'] in wids['characters']:
                print("Watching Attacker in "+killID)
                await killbot.send_message(channel, message)
                break
            else:
                vic = 1

        # Victim checking is easy.
        if vic == 1 and 'alliance' in victim and victim['alliance']['id_str'] in wids['alliances']:
            print("Watching Victim in "+killID)
            await killbot.send_message(channel, message)
        elif vic == 1 and 'corporation' in victim and victim['corporation']['id_str'] in wids['corps']:
            print("Watching Victim in "+killID)
            await killbot.send_message(channel, message)
        elif vic == 1 and 'character' in victim and victim['character']['id_str'] in wids['characters']:
            print("Watching Victim in "+killID)
            await killbot.send_message(channel, message)
        elif vic == 1 and victim['shipType']['id_str'] in wids['shipTypes']:
            print("Watching Ship Loss in "+killID)
            await killbot.send_message(channel, message)
        else:
            pass

        #await killbot.send_message(channel, counter)
        await asyncio.sleep(5)

if config.KILLWATCH_ENABLED == "TRUE":
    print(("Watching Corps:" + str(', '.join(config.watchids['corps']))+
    " | Alliances:" + str(', '.join(config.watchids['alliances']))+
     " | Characters:"+str(', '.join(config.watchids['characters']))+
     "\nShipGroups: "+str(', '.join(config.watchids['groups']))+
     " | ShipTypes: "+str(', '.join(config.watchids['shipTypes']))+
     "\nChannel:  " +str(config.KILLWATCH_CHANNEL)+"\n"))
    killbot.loop.create_task(watch_redisq(config.KILLWATCH_CHANNEL, config.watchids))
#----------------------------------------------------------------------

killbot.run(config.BOT_TOKEN)
