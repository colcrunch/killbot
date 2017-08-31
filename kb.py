import requests
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
    with async_timeout.timeout(10):
        async with session.get(url, headers=headers) as response:
            return await response.json()

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
