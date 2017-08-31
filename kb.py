import requests
import json
import datetime
import asyncio
import config
import sqlite3

import discord
from discord.ext.commands import Bot

async def getID(char):
    url = ("https://esi.tech.ccp.is/latest/search/?categories=character&datasource=tranquility&language=en-us&search="+ char +"&strict=true")
    print(url)
    r = requests.get(url)
    json = r.json()
    global cid
    if 'character' in json:
        idlist = json['character']
        cid = str(idlist[0])
    else:
        cid = "0"

async def get_stats():
    headers = {
        'user-agent': 'application: https://github.com/colcrunch/killbot contact: rhartnett35@gmail.com'
    }
    time = datetime.datetime.utcnow()
    top = time.strftime("%Y%m")
    url = ("https://zkillboard.com/api/stats/characterID/"+cid+"/")
    r = requests.get(url, headers=headers)
    select = r.json()
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
