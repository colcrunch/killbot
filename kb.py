import requests

URL = "no"

async def getID(char):
    URL = ("http://api.eveonline.com/eve/CharacterID.xml.aspx?names="+ char)
    print(URL)
