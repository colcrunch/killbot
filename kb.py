import requests
from xml.etree import ElementTree

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
    global url
    url = ("https://zkillboard.com/api/stats/characterID/"+cid+"/")
    r = requests.get(url, headers=headers)
    print(url)
