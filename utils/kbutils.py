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