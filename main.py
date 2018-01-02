#Import bot scripts
import config
import kb
import market
import systems
import guess
import esinfo

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
import urllib

counter = 0
start_time = datetime.datetime.utcnow()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discord'+start_time.strftime("%Y%m%d%H%M")+'.log', encoding='utf-8', mode='w')
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
    return await killbot.say("Pong!")

#---------------------------------------------------------------------
#   Bot Stats Command
#   Displays various statistics about the currnet bot.
#---------------------------------------------------------------------
@killbot.command(aliases=['bs'], pass_context=True)
async def botStats(ctx):
    """ Displpays various statistics about the bot"""
    servers = []
    for server in killbot.servers:
        servers.append(server)

    now = datetime.datetime.utcnow()

    uptime = now - start_time

    embed = discord.Embed(title="Bot Statistics", colour=discord.Colour.green())
    embed.set_author(name=killbot.user.name, icon_url=await esinfo.unWebp(killbot.user.avatar_url))
    embed.set_thumbnail(url=await esinfo.unWebp(killbot.user.avatar_url))
    embed.add_field(name="Servers", value=len(servers),inline=True)
    embed.add_field(name="Uptime", value=await strftdelta(uptime), inline=True)
    embed.add_field(name="Killmails Processed", value=counter, inline=False)

    return await killbot.send_message(ctx.message.channel, embed=embed)

async def strftdelta(tdelta):
    d = dict(days=tdelta.days)
    d['hrs'], rem = divmod(tdelta.seconds, 3600)
    d['min'], d['sec'] = divmod(rem, 60)

    if d['min'] is 0:
        fmt = '{sec} sec'
    elif d['hrs'] is 0:
        fmt = '{min} min {sec} sec'
    elif d['days'] is 0:
        fmt = '{hrs} hr(s) {min} min {sec} sec'
    else:
        fmt = '{days} day(s) {hrs} hr(s) {min} min {sec} sec'

    return fmt.format(**d)
#---------------------------------------------------------------------
# Eve Time command
# Returns the current EVE/UTC Time.
#---------------------------------------------------------------------
@killbot.command(aliases = ['eve_time', 'evetime', 'et'])
async def time():
    """Displays EVE/UTC time."""
    time = datetime.datetime.utcnow().strftime("%H:%M")
    return await killbot.say("Current EVE (UTC) Time: " + time)

#--------------------------------------------------------------------
#   Threat command
#    This command uses kb.py to get the killboard stats of a given character.
#--------------------------------------------------------------------
@killbot.command(aliases = ['t'])
async def threat(*, char: str):
    """ Gets stats for a character from zKill"""
    cid = await esinfo.esiID(char, 'char')
    if cid == "0":
        return await killbot.say("Character not found. Please check your spelling and try again.")
    else:
        stats = await kb.get_stats(cid)

    return await killbot.say(":alien: "+char+" \n\n :skull_crossbones: "+str(stats[0])+"  :children_crossing:"+str(stats[1])+" :knife: "+str(stats[2])+" :calendar:"+str(stats[3])+"\n\n\n :bookmark: "+stats[4])

@threat.error
async def threat_error(error, ctx):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        return await killbot.say("You must specify a character to look up.")
    else:
        print(error)
        logger.error("There was an error with the threat command!: \n"+str(error))
        return await killbot.say("Please contact Col Crunch about the following error (make sure to include the exact command that caused it.) \n\n*** Error: ***  "+str(error))
#----------------------------------------------------------------------
# Info command
# This command returns public info from ESI.
#----------------------------------------------------------------------
@killbot.group(aliases=['i', 'inf'], pass_context=True)
async def info(ctx):
    """ Returns public info from ESI """
    pass

# Subcommand for character info
@info.command(name="character", aliases=['char', 'ch'], pass_context=True)
async def character(ctx, *, char: str):
    """ Returns public info for a character from ESI """
    eid = await esinfo.esiID(char, 'char')
    if eid == '0':
        return await killbot.say("Character not found, please check your spelling and try again.")

    inf = await esinfo.esiChar(eid)
    corpName = await kb.esiName(inf[0], 'ent')
    urlChar = urllib.parse.quote_plus(char)

    kbUrl = "https://zkillboard.com/character/{}/".format(eid)
    ewUrl = "https://evewho.com/pilot/{}".format(urlChar)

    embed = discord.Embed(title="{} Character Info".format(inf[2]),description="‌‌ ", colour=discord.Colour.dark_blue())
    embed.set_author(name=killbot.user.name, icon_url=await esinfo.unWebp(killbot.user.avatar_url))
    embed.set_thumbnail(url="https://imageserver.eveonline.com/Character/{}_128.jpg".format(eid))
    embed.add_field(name="Corporation", value=corpName, inline=True)
    if inf[3] is not None:
        allyName = await kb.esiName(inf[3], 'ent')
        embed.add_field(name="Alliance", value=allyName, inline=True)
    embed.add_field(name="Birthdate", value=inf[1], inline=False)
    embed.add_field(name="Additional Information", value=kbUrl+"\n"+ewUrl, inline= False)

    return await killbot.send_message(ctx.message.channel, embed=embed)

# Subcommand for Corp info
@info.command(name="corporation", aliases=['corp', 'co'], pass_context=True)
async def corporation(ctx, *, corp: str):
    """ Returns public info for a corp from ESI """
    eid = await esinfo.esiID(corp, 'corp')
    if eid == '0':
        return await killbot.say("Corporation not found, please check your spelling and try again.")

    inf = await esinfo.esiCorp(eid)

    zkb = "https://zkillboard.com/corporation/{}/".format(eid)
    dotlan = "https://evemaps.dotlan.net/corp/{}".format(eid)

    ceo = await kb.esiName(inf[3], 'char')

    embed = discord.Embed(title="{} Corporation Info".format(inf[0]),description="‌‌ ", colour=discord.Colour.green())
    embed.set_author(name=killbot.user.name, icon_url=await esinfo.unWebp(killbot.user.avatar_url))
    embed.set_thumbnail(url="https://imageserver.eveonline.com/Corporation/{}_128.png".format(eid))
    embed.add_field(name="Ticker", value='[{}]'.format(inf[1]), inline=True)
    embed.add_field(name="Member Count", value=inf[2], inline=True)
    embed.add_field(name="CEO", value=inf[3], inline=True)
    embed.add_field(name="Founded", value=inf[4], inline=True)
    if inf[5] is not None:
        allyName = await kb.esiName(inf[5], 'ent')
        embed.add_field(name="Alliance", value=allyName, inline=True)

    if inf[6] is not None:
        embed.add_field(name="Website", value=inf[6], inline=False)
    embed.add_field(name="Additional Info", value=zkb+"\n"+dotlan, inline=False)

    return await killbot.send_message(ctx.message.channel, embed=embed)

# Subcommand for Alliance info
@info.command(name="alliance", aliases=['a', 'ally'], pass_context=True)
async def alliance(ctx, *, ally: str):
    """ Returns public info for an alliance from ESI """
    eid = await esinfo.esiID(ally, 'ally')
    if eid == '0':
        return await killbot.say("Alliance not found, please check your spelling and try again.")

    inf = await esinfo.esiAlly(eid)

    zkb = "https://zkillboard.com/alliance/{}/".format(eid)
    dotlan = "https://evemaps.dotlan.net/alliance/{}".format(eid)

    exe = await kb.esiName(inf[2], 'ent')

    embed = discord.Embed(title="{} Alliance Info".format(inf[0]), description="‌‌ ", colour=discord.Colour.blue())
    embed.set_author(name=killbot.user.name, icon_url=await esinfo.unWebp(killbot.user.avatar_url))
    embed.set_thumbnail(url="https://imageserver.eveonline.com/Alliance/{}_128.png".format(eid))
    embed.add_field(name="Ticker", value=inf[1], inline=True)
    embed.add_field(name="Exec Corp", value=exe, inline=True)
    embed.add_field(name="Founded", value=inf[3], inline=False)

    return await killbot.send_message(ctx.message.channel, embed=embed)


#----------------------------------------------------------------------
# Price Check command
# This command checks jita prices for the given item against the eve-central API
#----------------------------------------------------------------------
async def flats(item, region_name):
    #Apparantly the name "REGION" is not acceptable as a function name?
    #Actual logic for price checking... maybe just move to market.py?
    print(region_name)
    regionID = await market.getRegion(region_name)
    shortcut = guess.shortcuts

    if item == '':
        return await killbot.say("You must specify an item to look up!")

    print(item)
    if item.lower() in shortcut:
        itemID = await market.getID(shortcut[item.lower()])
        item = shortcut[item.lower()]
    else:
        itemID = await market.getID(item)
        if itemID is "None":
            return await killbot.say("Item not found, please check your spelling and try again.")

    if regionID is "None":
        return await killbot.say("Region not found. Please check your spelling and try again.")
    else:
        info = await market.getPrices(itemID, regionID)

    priceinfo = info[0]
    avgs = info[1]
    plex_msg = ""
    if item.lower() == "plex":
        buy_avg = str('{:,}'.format(avgs[0]*500))
        sell_avg = str('{:,}'.format(avgs[1]*500))
        plexinfo = [buy_avg, sell_avg]
        plex_msg = "**Monthly Sub Cost**  \n ***Sell Avg:*** "+plexinfo[1]+"   ***Buy Avg:*** "+plexinfo[0]+"\n\n "

    return await killbot.say(" :chart_with_upwards_trend:  "+ item +"  :map: "+region_name.title()+"\n\n "+plex_msg+":regional_indicator_b:     ***Max:*** "+priceinfo[1]+"  ***Min:*** "+priceinfo[0]+"  ***Avg:*** "+priceinfo[2]+" \n :regional_indicator_s:     ***Max:*** "+priceinfo[4]+" ***Min:*** "+priceinfo[3]+" ***Avg:*** "+priceinfo[5]+" \n\n :bookmark: https://evemarketer.com/types/"+itemID )


@killbot.group(aliases = ['pc'], pass_context=True)
async def price_check(ctx, *item):
    """ Checks prices for specified items in a specified region. (Default: The Forge) """

    item = list(item)
    if prefix+'r' in item:
        i = item.index(prefix+'r')
        item_list = item[:i]
        region_list = item[i+1:]
        item = " ".join(item_list)
        region_name = " ".join(region_list)
        return await flats(item, region_name)
    elif prefix+'region' in item:
        i = item.index(prefix+'region')
        item_list = item[:i]
        region_list = item[i+1:]
        item = " ".join(item_list)
        region_name = " ".join(region_list)
        return await flats(item, region_name)
    else:
        region_name = 'The Forge'
        it = " ".join(item)
        item = it
        return await flats(item, region_name)

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
    sysid = await systems.getID(sys)
    if sID == None :
        return await killbot.say("System Not Found! Please check your spelling and try again!")
    else:
        stats = await systems.getStats(sID)

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
    global counter
    await killbot.wait_until_ready()
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
            counter += 1
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
