from utils.importsfile import *


async def get_price(item, region):
    if region is None:
        url = f'http://api.evemarketer.com/ec/marketstat/json?typeid={item}'
    else:
        url = f'http://api.evemarketer.com/ec/marketstat/json?typeid={item}&regionlimit={region}'

    async with aiohttp.ClientSession() as session:
        resp = await core.get_json(session, url)

    respi = dict(resp[0])
    sell = respi['sell']
    buy = respi['buy']

    bMin = buy['min']
    bMax = buy['max']
    bAvg = buy['avg']

    sMin = sell['min']
    sMax = sell['max']
    sAvg = sell['avg']

    lst = [bMin, bMax, bAvg, sMin, sMax, sAvg]
    new = []
    for i in range(len(lst)):
        new.append('{:,}'.format(round(lst[i], 2)))

    price = {'bMin': new[0],
             'bMax': new[1],
             'bAvg': new[2],
             'sMin': new[3],
             'sMax': new[4],
             'sAvg': new[5],
             'plex': [sAvg, bAvg]}

    return price
