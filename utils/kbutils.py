from utils.importsfile import *


async def get_mail(kid):
    url = f'http://zkillboard.com/api/killID/{kid}/'
    async with aiohttp.ClientSession() as session:
        resp = await core.get_json(session, url)

    km = resp[0]
    time = datetime.datetime.strptime(km['killmail_time'], '%Y-%m-%dT%H:%M:%SZ')
    victim = km['victim']
    loc = km['solar_system_id']
    value = '{:,}'.format(km['zkb']['totalValue'])
    attack = km['attackers']

    return {'time': time, 'victim': victim, 'location': loc, 'value': value, 'attackers': attack}

async def get_stats(cid):
    url = f'http://zkillboard.com/api/stats/characterID/{cid}/'
    async with aiohttp.ClientSession() as session:
        resp = await core.get_json(session, url)

    stats = resp
    if 'shipsDestroyed' in stats:
        gRatio = stats['gangRatio']
        dRatio = stats['dangerRatio']
        iskD = stats['iskDestroyed']
        iskL = stats['iskLost']
        kills = stats['shipsDestroyed']
        losses = stats['shipsLost']
    else:
        gRatio = None
        dRatio = None
        iskD = None
        iskL = None
        kills = None
        losses = None
    month = datetime.datetime.utcnow().strftime('%Y%m')

    if 'months' in stats:
        months = stats['months']
        if month in months:
            kMonth = months[month]['shipsDestroyed']
            lMonth = months[month]['shipsLost']
            month = {'kills': kMonth, 'losses': lMonth}
        else:
            month = None
    else:
        month = None

    data = {'kills': kills,
            'losses': losses,
            'gangRatio': gRatio,
            'dangerRatio': dRatio,
            'iskDestroyed': iskD,
            'iskLost': iskL,
            'month': month}

    return data
