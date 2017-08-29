import requests
import datetime
from xml.etree import ElementTree
import sqlite3

async def getID(item):
    url = ("https://api.eve-marketdata.com/api/type_id.xml?char_name=Troy Aihaken&v="+item)
    r = requests.get(url)
    tree = ElementTree.fromstring(r.content)
    global itemID
    itemID = tree.find("val").text

async def getPrices(itemID):
    url = ("http://api.eve-central.com/api/marketstat/json?typeid="+itemID+"&usesystem=30000142")
    r = requests.get(url)
    price = r.json()
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