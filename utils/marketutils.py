from utils.importsfile import *


async def get_price(item, region):
    if region is None:
        url = f'http://api.evemarketer.com/ec/marketstat/json?typeid={item}'
    else:
        url = f'http://api.evemarketer.com/ec/marketstat/json?typeid={item}&regionlimit={region}'

    async with aiohttp.ClientSession() as session:
        resp = await core.get_json(session, url)
    resp = resp['resp']
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


async def build(info, item, item_id, region):
    if region is None:
        embed = discord.Embed(title=f'{item} Market Information')
    else:
        embed = discord.Embed(title=f'{item} - {region} Market Information')
    embed.set_author(name='EveMarketer', icon_url='https://evemarketer.com/static/img/logo_32.png',
                     url=f'https://evemarketer.com/types/{item_id}')
    embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Type/{item_id}_64.png')
    embed.add_field(name="Sell Min", value=info['sMin'], inline=True)
    embed.add_field(name="Sell Max", value=info['sMax'], inline=True)
    if item.lower() == 'plex':
        embed.add_field(name='Sell Avg', value=info['sAvg'], inline=True)
        embed.add_field(name='Monthly Sub Sell Avg', value='{:,}'.format(round(info['plex'][0] * 500, 2)), inline=True)
    else:
        embed.add_field(name='Sell Avg', value=info['sAvg'], inline=False)
    embed.add_field(name='Buy Min', value=info['bMin'], inline=True)
    embed.add_field(name='Buy Max', value=info['bMax'], inline=True)
    if item.lower() == 'plex':
        embed.add_field(name='Buy Avg', value=info['bAvg'], inline=True)
        embed.add_field(name='Monthly Sub Buy Avg', value='{:,}'.format(round(info['plex'][1] * 500, 2)), inline=True)
    else:
        embed.add_field(name='Buy Avg', value=info['bAvg'], inline=True)

    return embed