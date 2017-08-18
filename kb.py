import requests
from xml.etree import ElementTree
import json
import datetime

async def getID(char):
    url = ("http://api.eveonline.com/eve/CharacterID.xml.aspx?names="+ char)
    print(url)
    response = requests.get(url)
    tree = ElementTree.fromstring(response.content)
    for row in tree.iter('row'):
        att = row.attrib

    global cid
    cid = att['characterID']

async def get_stats():
    headers = {
        'user-agent': 'application: https://github.com/colcrunch/killbot contact: rhartnett35@gmail.com'
    }
    time = datetime.datetime.utcnow()
    top = time.strftime("%Y%m")
    url = ("https://zkillboard.com/api/stats/characterID/"+cid+"/")
    r = requests.get(url, headers=headers)
    select = r.json()
    danger = select["dangerRatio"]
    gang = select["gangRatio"]
    kills_all = select["allTimeSum"]
    kills_mo = select["months"][top]["shipsDestroyed"]
    global stats
    stats = [danger, gang, kills_all, kills_mo]
    global kburl
    kburl = ("http://zkillboard.com/character/"+cid)
