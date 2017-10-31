import json
import datetime
import asyncio
import config
import sqlite3
import urllib

import aiohttp
import async_timeout

import discord
from discord.ext.commands import Bot

async def fetch(session, url):
    headers = {'user-agent': 'application: https://github.com/colcrunch/killbot contact: rhartnett35@gmail.com','content-type': 'application/json'}
    with async_timeout.timeout(15):
        async with session.get(url, headers=headers) as response:
            return await response.json()

async def buildMsg(killmail):
    attackers = killmail['package']['killmail']['attackers']
    killID= str(killmail['package']['killID'])
    victim = killmail['package']['killmail']['victim']
    solarSystem = killmail['package']['killmail']['solar_system_id']
    solName = await getSolName(solarSystem)
    timeStr = killmail['package']['killmail']['killmail_time']
    timeTime = datetime.datetime.strptime(timeStr, '%Y-%m-%dT%H:%M:%SZ')
    val = '{:,}'.format(killmail['package']['zkb']['totalValue'])
    # Find the final blow and get the alliance or corp ID
    for attacker in attackers:
        if attacker['final_blow'] is True:
            if 'alliance_id' in attacker:
                fbAlly = attacker['alliance_id']
                fbAllyName = await esiName(fbAlly, 'ent')
                fbCorp = attacker['corporation_id']
                fbCorpName = await esiName(fbCorp, 'ent')
                fbChar = attacker['character_id']
                fbCharName = await esiName(fbChar, 'ent')
                final_blow = [fbAllyName, fbCorpName, fbCharName]
            else:
                fbCorp = attacker['corporation_id']
                fbCorpName = await esiName(fbCorp, 'ent')
                fbChar = attacker['character_id']
                fbCharName = await esiName(fbChar, 'ent')
                final_blow = [None, fbCorpName, fbCharName]
        else:
            pass
    vicID = victim['character_id']
    vicCorpID = victim['corporation_id']
    vicCorpName = await esiName(vicCorpID, 'ent')
    vicName = await esiName(vicID, 'char')
    vicShip = victim['ship_type_id']
    shipRender = 'https://image.eveonline.com/Render/'+str(vicShip)+'_64.png'
    shipName = await getShip(vicShip)
    link = "https://zkillboard.com/kill/"+killID+"/"

    #Actually make the message
    Msg = discord.Embed(title=vicName+' ('+vicCorpName+') lost their '+shipName, timestamp=timeTime)
    Msg.set_thumbnail(url=shipRender)
    if final_blow[0] is not None:
        #final blow fields
        corpStr = final_blow[1]+' ('+final_blow[0]+')'
        Msg.add_field(name="Final Blow", value=final_blow[2], inline=True)
        Msg.add_field(name="Corp", value=corpStr, inline=True)
        #Msg.add_field(name=" ", value=" ", inline=True)
    elif final_blow[0] is None:
        #final blow feilds
        Msg.add_field(name="Final Blow", value=final_blow[2], inline=True)
        Msg.add_field(name="Corp", value=final_blow[1], inline=True)
        #Msg.add_field(name=" ", value=" ", inline=True)
    vISK = str(val)+" ISK"
    Msg.add_field(name="Value", value=vISK, inline=False)
    Msg.add_field(name="System", value=solName, inline=True)
    Msg.set_author(name="zKillboard", url='http://zkillboard.com', icon_url='https://zkillboard.com/img/wreck.png')
    return Msg

async def getSolName(sysID):
    sID = str(sysID)
    conn = sqlite3.connect('sde.sqlite')
    c = conn.cursor()
    c.execute("SELECT solarSystemName FROM mapSolarSystems WHERE solarSystemID = "+sID)
    s = c.fetchone()
    name = s[0]
    conn.close()
    return name

async def getShip(typeID):
    tID = str(typeID)
    conn = sqlite3.connect('sde.sqlite')
    c = conn.cursor()
    c.execute("SELECT typeName FROM invTypes WHERE typeID = "+tID)
    s = c.fetchone()
    nm = s[0]
    conn.close()
    return nm

async def esiName(nID, rl):
    urlchar = 'https://esi.tech.ccp.is/latest/characters/names/?character_ids='+str(nID)+'&datasource=tranquility'
    urlent = 'https://esi.tech.ccp.is/latest/alliances/names/?alliance_ids='+str(nID)+'&datasource=tranquility'
    if rl == "char":
        url = urlchar
        nm = 'character_name'
    elif rl == 'ent':
        url = urlent
        nm = 'alliance_name'
    async with aiohttp.ClientSession() as session:
        resp = await fetch(session, url)
    n = resp[0]
    name = n[nm]
    return name


async def getID(char):
    urlchar = urllib.parse.quote_plus(char)
    async with aiohttp.ClientSession() as session:
        json = await fetch(session, "https://esi.tech.ccp.is/latest/search/?categories=character&datasource=tranquility&language=en-us&search="+urlchar+"&strict=true")
        print(json)
    global cid
    if 'character' in json:
        idlist = json['character']
        cid = str(idlist[0])
    else:
        cid = "0"

async def get_stats():
    time = datetime.datetime.utcnow()
    top = time.strftime("%Y%m")
    async with aiohttp.ClientSession() as session:
        select = await fetch(session, "https://zkillboard.com/api/stats/characterID/"+cid+"/")
    if 'dangerRatio' in select:
        danger = select["dangerRatio"]
    else:
        danger = "NoData"
    if 'gangRatio' in select:
        gang = select["gangRatio"]
    else:
        gang = "No Data"
    if 'allTimeSum' in select:
        kills_all = select["allTimeSum"]
    else:
        kills_all = "<  100"
    if 'months' in select:
        months = select['months']
        if top in months:
            kills_mo = select["months"][top]["shipsDestroyed"]
        else:
            kills_mo = "No Kills Yet"
    else:
        kills_mo = "No Kills Yet"
    global stats
    stats = [danger, gang, kills_all, kills_mo]
    global kburl
    kburl = ("http://zkillboard.com/character/"+cid)
