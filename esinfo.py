import json
import datetime
import asyncio
import config
import sqlite3
import urllib
import kb

import aiohttp
import async_timeout

import discord
from discord.ext.commands import Bot

async def esiID(name, ref):
    urlName = urllib.parse.quote_plus(name)
    if ref == 'char':
        url = "https://esi.tech.ccp.is/latest/search/?categories=character&datasource=tranquility&language=en-us&search={}&strict=true".format(urlName)
        kind = 'character'
    elif ref == 'corp':
        url = "https://esi.tech.ccp.is/latest/search/?categories=corporation&datasource=tranquility&language=en-us&search={}&strict=true".format(urlName)
        kind = 'corporation'
    elif ref == 'ally':
        url = "https://esi.tech.ccp.is/latest/search/?categories=alliance&datasource=tranquility&language=en-us&search={}&strict=true".format(urlName)
        kind = 'alliance'

    async with aiohttp.ClientSession() as session:
        resp = await kb.fetch(session, url)
    if kind in resp:
        eid = str(resp[kind][0])
    else:
        eid = '0'
    return eid

async def esiChar(eid):
    url = "https://esi.tech.ccp.is/v4/characters/{}/?datasource=tranquility".format(eid)
    async with aiohttp.ClientSession() as session:
        resp = await kb.fetch(session, url)
    corpID = resp['corporation_id']
    dob = resp['birthday']
    name = resp['name']
    if 'alliance_id' in resp:
        allyID = resp['alliance_id']
    else:
        allyID = None
    inf = [corpID, dob, name, allyID]
    return inf

async def esiCorp(eid):
    url = "https://esi.tech.ccp.is/v4/corporations/{}/?datasource=tranquility".format(eid)
    async with aiohttp.ClientSession() as session:
        resp = await kb.fetch(session, url)
    name = resp['name']
    ticker = resp['ticker']
    mem = resp['member_count']
    ceoID = resp['ceo_id']
    if 'alliance_id' in resp:
        allyID = resp['alliance_id']
    else:
        allyID = None
    if resp['url'] == 'http://' or resp['url'] == '' or resp['url'] == 'https://':
        url = None
    else:
        url = resp['url']
    founded = resp['date_founded']
    inf = [name, ticker, mem, ceoID, founded, allyID, url]
    return inf

async def esiAlly(eid):
    url = "https://esi.tech.ccp.is/v3/alliances/{}/?datasource=tranquility".format(eid)
    async with aiohttp.ClientSession() as session:
        resp = await kb.fetch(session, url)
    name = resp['name']
    ticker = resp['ticker']
    exe = resp['executor_corporation_id']
    founded = resp['date_founded']
    inf = [name, ticker, exe, founded]
    return inf
