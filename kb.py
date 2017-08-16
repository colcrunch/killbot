import requests

async def getID(char):
    global URL
    URL = ("http://api.eveonline.com/eve/CharacterID.xml.aspx?names="+ char)
    print(URL)
