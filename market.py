import datetime
import kb
import sqlite3
import aiohttp

async def getID(item):
    conn = sqlite3.connect('sde.sqlite')
    c = conn.cursor()
    i = (item,)
    c.execute('SELECT typeID, groupID FROM invTypes WHERE typeName LIKE ?',i)
    t = c.fetchone()
    print(t)
    conn.close()
    if t is None:
        itemID = "None"
    else:
        itemID = str(t[0])
    return itemID

async def getRegion(region):
    conn = sqlite3.connect('sde.sqlite')
    c = conn.cursor()
    r = (region,)
    c.execute('SELECT regionID FROM mapRegions WHERE regionName LIKE ?',r)
    t = c.fetchone()
    print(t)
    conn.close()
    if t is None:
        regionID = "None"
    else:
        regionID = str(t[0])
    return regionID

async def getPrices(itemID, region):
    async with aiohttp.ClientSession() as session:
        price = await kb.fetch(session, "http://api.evemarketer.com/ec/marketstat/json?typeid="+itemID+"&regionlimit="+region)
    prices = dict(price[0])
    buy_min = str('{:,}'.format(round(prices['buy']['min'], 2)))
    buy_max = str('{:,}'.format(round(prices['buy']['max'], 2)))
    sell_min = str('{:,}'.format(round(prices['sell']['min'], 2)))
    sell_max = str('{:,}'.format(round(prices['sell']['max'], 2)))
    buy_avg = str('{:,}'.format(round(prices['buy']['avg'], 2)))
    sell_avg  = str('{:,}'.format(round(prices['sell']['avg'], 2)))
    global priceinfo
    priceinfo = [buy_min, buy_max, buy_avg, sell_min, sell_max, sell_avg]
    global avgs
    avgs = [round(prices['buy']['avg'], 2), round(prices['sell']['avg'], 2)]
    print(priceinfo)
