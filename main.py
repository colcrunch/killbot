#Import bot scripts
import config
import kb
import market
import systems

#Import discord python library
import discord
from discord.ext.commands import Bot

#Import other libraries needed
import datetime
import asyncio
import aiohttp
import sqlite3
import logging
import re

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discord'+datetime.datetime.utcnow().strftime("%Y%m%d%H%M")+'.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s ::: %(levelname)s ::: %(name)s :::  %(message)s'))
logger.addHandler(handler)

killbot = Bot(command_prefix=config.PREFIX)
prefix = config.PREFIX

@killbot.event
async def on_ready():
    print("Bot online")
    print('------')
    print('Logged in as')
    print(killbot.user.name)
    print(killbot.user.id)
    print('------')
    await killbot.change_presence(game=discord.Game(type=0,name=config.msg+' | '+config.PREFIX+'help'), afk=False)

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
        logger.error("There was an error with the threat command!: \n"+error)
        return await killbot.say("Please contact Col Crunch about the following error (make sure to include the exact command that caused it.) \n\n*** Error: ***  "+str(error))

#----------------------------------------------------------------------
# Price Check command
# This command checks jita prices for the given item against the eve-central API
#----------------------------------------------------------------------
async def flats(item, region_name):
    #Apparantly the name "REGION" is not acceptable as a function name?
    print(region_name)
    regionID = await market.getRegion(region_name)
    itemID = await market.getID(item)
    if regionID is "None":
        return await killbot.say("Region not found. Please check your spelling and try again.")
    else:
        await market.getPrices(itemID, regionID)

    priceinfo = market.priceinfo
    plex_msg = ""
    if item_price.lower() == "plex":
        buy_avg = str('{:,}'.format(market.avgs[0]*500))
        sell_avg = str('{:,}'.format(market.avgs[1]*500))
        plexinfo = [buy_avg, sell_avg]
        plex_msg = "**Monthly Sub Cost**  \n ***Sell Avg:*** "+plexinfo[1]+"   ***Buy Avg:*** "+plexinfo[0]+"\n\n "

    return await killbot.say(" :chart_with_upwards_trend:  "+ item_price +"  :map: "+region_name.title()+"\n\n "+plex_msg+":regional_indicator_b:     ***Max:*** "+priceinfo[1]+"  ***Min:*** "+priceinfo[0]+"  ***Avg:*** "+priceinfo[2]+" \n :regional_indicator_s:     ***Max:*** "+priceinfo[4]+" ***Min:*** "+priceinfo[3]+" ***Avg:*** "+priceinfo[5]+" \n\n :bookmark: https://evemarketer.com/types/"+itemID )


@killbot.group(aliases = ['pc'], pass_context=True)
async def price_check(ctx, *item):
    """ Checks prices for specified items in a specified region. (Default: The Forge) """
    global item_price

    item = list(item)
    if prefix+'r' in item:
        i = item.index(prefix+'r')
        item_list = item[:i]
        region_list = item[i+1:]
        item = " ".join(item_list)
        region_name = " ".join(region_list)
        item_price = item
        return await flats(item, region_name)
    elif prefix+'region' in item:
        i = item.index(prefix+'region')
        item_list = item[:i]
        region_list = item[i+1:]
        item = " ".join(item_list)
        region_name = " ".join(region_list)
        item_price = item
        return await flats(item, region_name)
    else:
        region = '10000002'
        it = " ".join(item)
        item = it
        print(item)
        itemID = await market.getID(item)
        if itemID == "None":
            return await killbot.say("Item not found. Please check your spelling and try again.")
        else:
            await market.getPrices(itemID, region)

        priceinfo = market.priceinfo
        plex_msg = ""
        if item.lower() == "plex":
            buy_avg = str('{:,}'.format(market.avgs[0]*500))
            sell_avg = str('{:,}'.format(market.avgs[1]*500))
            plexinfo = [buy_avg, sell_avg]
            plex_msg = "**Monthly Sub Cost**  \n ***Sell Avg:*** "+plexinfo[1]+"   ***Buy Avg:*** "+plexinfo[0]+"\n\n "

        return await killbot.say(" :chart_with_upwards_trend:  "+ item +" :map: The Forge\n\n "+plex_msg+":regional_indicator_b:     ***Max:*** "+priceinfo[1]+"  ***Min:*** "+priceinfo[0]+"  ***Avg:*** "+priceinfo[2]+" \n :regional_indicator_s:     ***Max:*** "+priceinfo[4]+" ***Min:*** "+priceinfo[3]+" ***Avg:*** "+priceinfo[5]+" \n\n :bookmark: https://evemarketer.com/types/"+itemID )
#Not a real "command" as it will never be called as such.
@price_check.command(name=prefix+"region",aliases = [prefix+'r'])
async def place_holder():
    """ Use this subcommand to specify a region to be checked. """
    pass

@price_check.error
async def pc_error(error, ctx):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        return await killbot.say("You must specify an item to look up!")
    else:
        logger.error("There was an error with the price check command!:")
        logger.error(error)
        print(error)
        return await killbot.say("Please contact Col Crunch about the following error (make sure to include the exact command that caused it.) \n\n *** Error: ***  "+ str(error))

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
#System command
# Command to show system stats
#----------------------------------------------------------------------
@killbot.command(aliases=['sys'])
async def system(*, sys: str):
    """Prints system stats (Not available for WH systems)"""
    if config.system_cmd.lower() == 'db':
        sys_msg = "The following are system stats for the last 24h."
    elif config.system_cmd.lower() == 'esi':
        sys_msg = "The following are system stats for the last 1h."
    else:
        logger.error("Config variable system_cmd not properly configured! "+config.system_cmd+" is not a valid option.")
        return await killbot.say("Config variable system_cmd not properly configured! "+config.system_cmd+" is not a valid option.")

    if re.match(r'[Jj]([0-9]{6})', sys) is not None or sys == "Thera":
        return await killbot.say("Data not available for Wormhole systems.")
    await systems.getID(sys)
    sID = systems.systemID
    if sID == None :
        return await killbot.say("System Not Found! Please check your spelling and try again!")
    else:
        await systems.getStats(sID)

    stats = systems.stats
    if stats == None :
        logger.error("Stats not found! Please make sure the bot is configured properly. (DB vs ESI pulls)")
        return await killbot.say("Stats not found! Please make sure the bot is configured properly.")

    return await killbot.say(""+sys_msg+" \n\n :regional_indicator_k: **Ship Kills:** "+str(stats[0])+" **NPC Kills:** "+str(stats[1])+" **Pod Kills:** "+str(stats[2])+"\n :regional_indicator_j: **Jumps:** "+str(stats[3])+"\n\n :bookmark: http://evemaps.dotlan.net/system/"+sys)

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
    logger.info(" Killboard watching started")
    wids = config.watchids
    await killbot.wait_until_ready()
    counter = 0
    channel = discord.Object(id=chid)
    try:
        while not killbot.is_closed:
            url = "https://redisq.zkillboard.com/listen.php"
            async with aiohttp.ClientSession() as session:
                kills = await kb.fetch(session, url)
            if kills['package'] is not None :
                # Set variables for parsing
                attackers = kills['package']['killmail']['attackers']
                killID= str(kills['package']['killID'])
                victim = kills['package']['killmail']['victim']
                #Build the message
                message = "https://zkillboard.com/kill/"+killID+"/"
                print(killID)
                logger.info("KillID: "+killID)
                # For deciding if I need to check the victim, and prevent double posting.
                attacks = len(attackers)
                vic = 0
                #Are we tracking any of the groups that are the attackers?
                for attacker in attackers:
                    if 'alliance_id' in attacker and str(attacker['alliance_id']) in wids['alliances']:
                        print("Watching Attacker in "+killID)
                        logger.info("Watching Attacker in "+killID)
                        embed = await kb.buildMsg(kills)
                        await killbot.send_message(channel, content=message, embed=embed)
                        break
                    elif 'corporation_id' in attacker and str(attacker['corporation_id']) in wids['corps']:
                        print("Watching Attacker in "+killID)
                        logger.info("Watching Attacker in "+killID)
                        embed = await kb.buildMsg(kills)
                        await killbot.send_message(channel, content=message, embed=embed)
                        break
                    elif 'character' in attacker and str(attacker['character_id']) in wids['characters']:
                        print("Watching Attacker in "+killID)
                        logger.info("Watching Attacker in "+killID)
                        embed = await kb.buildMsg(kills)
                        await killbot.send_message(channel, content=message, embed=embed)
                        break
                    else:
                        vic += 1

                # Victim checking is easy.
                if vic == attacks and 'alliance_id' in victim and str(victim['alliance_id']) in wids['alliances']:
                    print("Watching Victim in "+killID)
                    logger.info("Watching Victim in "+killID)
                    embed = await kb.buildMsg(kills)
                    await killbot.send_message(channel, content=message, embed=embed)
                elif vic == attacks and 'corporation_id' in victim and str(victim['corporation_id']) in wids['corps']:
                    print("Watching Victim in "+killID)
                    logger.info("Watching Victim in "+killID)
                    embed = await kb.buildMsg(kills)
                    await killbot.send_message(channel, content=message, embed=embed)
                elif vic == attacks and 'character_id' in victim and str(victim['character_id']) in wids['characters']:
                    print("Watching Victim in "+killID)
                    logger.info("Watching Victim in "+killID)
                    embed = await kb.buildMsg(kills)
                    await killbot.send_message(channel, content=message, embed=embed)
                elif vic == attacks and str(victim['ship_type_id']) in wids['shipTypes']:
                    print("Watching Ship Loss in "+killID)
                    logger.info("Watching Victim in "+killID)
                    embed = await kb.buildMsg(kills)
                    await killbot.send_message(channel, content=message, embed=embed)
                else:
                    pass
            else:
                pass

            #await killbot.send_message(channel, counter)
            await asyncio.sleep(5)

    except Exception as error:
        logger.critical("Exception occured in watch_redisq!")
        logger.critical(error)
        killbot.loop.create_task(watch_redisq(config.KILLWATCH_CHANNEL, config.watchids))

if config.KILLWATCH_ENABLED == "TRUE":
    print(("Watching \nCorps:" + str(', '.join(config.watchids['corps']))+
    " | Alliances:" + str(', '.join(config.watchids['alliances']))+
     " | Characters:"+str(', '.join(config.watchids['characters']))+
     "\nShipGroups: "+str(', '.join(config.watchids['groups']))+
     " | ShipTypes: "+str(', '.join(config.watchids['shipTypes']))+
     "\nChannel:  " +str(config.KILLWATCH_CHANNEL)+"\n"))
    killbot.loop.create_task(watch_redisq(config.KILLWATCH_CHANNEL, config.watchids))
#----------------------------------------------------------------------

killbot.run(config.BOT_TOKEN)
