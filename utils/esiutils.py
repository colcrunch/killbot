from utils.importsfile import *
from utils.core import get_json as get


async def get_id(name, ref):
    urlName = urllib.parse.quote_plus(name)
    defs = {'ally': 'alliance',
            'corp': 'corporation',
            'char': 'character',
            'itype': 'inventory_type',
            'solsystem': 'solar_system',
            'region': 'region',
            'faction': 'faction',
            'agent': 'agent',
            'con': 'constellation',
            'station': 'station'}
    url = f'https://esi.tech.ccp.is/v2/search/?categories={defs[ref]}&datasource=tranquility&search={urlName}' \
          f'&strict=true'

    async with aiohttp.ClientSession() as session:
        resp = await get(session, url)
    if defs[ref] in resp:
        eid = str(resp[defs[ref]][0])
    else:
        eid = None
    return eid


async def esi_char(eid):
    url = f'https://esi.tech.ccp.is/v4/characters/{eid}/?datasource=tranquility'
    async with aiohttp.ClientSession() as session:
        resp = await get(session, url)
    corpID = resp['corporation_id']
    dob = datetime.datetime.strptime(resp['birthday'], '%Y-%m-%dT%H:%M:%SZ')
    now = datetime.datetime.utcnow()
    age = now - dob
    name = resp['name']
    gender = resp['gender']
    sec = resp['security_status']

    inf = {'corpid': corpID,
           'dob': dob,
           'age': age,
           'name': name,
           'gender': gender,
           'sec': sec}

    return inf


async def esi_corp(eid):
    url = f'https://esi.tech.ccp.is/v4/corporations/{eid}/?datasource=tranquility'
    async with aiohttp.ClientSession() as session:
        resp = await get(session, url)
    name = resp['name']
    ticker = resp['ticker']
    member = resp['member_count']
    ceoid = resp['ceo_id']
    if 'alliance_id' in resp:
        ally = resp['alliance_id']
    else:
        ally = None
    dob = datetime.datetime.strptime(resp['date_founded'], '%Y-%m-%dT%H:%M:%SZ')
    if resp['url'] == 'http://' or resp['url'] == '' or resp['url'] == 'https://':
        url = None
    else:
        url = resp['url']

    inf = {'name': name,
           'ticker': ticker,
           'member': member,
           'ceoid': ceoid,
           'dob': dob,
           'url': url,
           'ally': ally}

    return inf


async def esi_ally(eid):
    url = f'https://esi.tech.ccp.is/v3/alliances/{eid}/?datasource=tranquility'
    async with aiohttp.ClientSession() as session:
        resp = await get(session, url)
    name = resp['name']
    founder = resp['creator_id']
    create_corp = resp['creator_corporation_id']
    ticker = resp['ticker']
    founded = datetime.datetime.strptime(resp['date_founded'], '%Y-%m-%dT%H:%M:%SZ')
    exec_corp = resp['executor_corporation_id']

    inf = {
        'name': name,
        'founder': founder,
        'create_corp': create_corp,
        'ticker': ticker,
        'founded': founded,
        'exec': exec_corp
    }

    return inf


async def esi_status():
    url = "https://esi.tech.ccp.is/latest/status/?datasource=tranquility"
    async with aiohttp.ClientSession() as session:
        resp = await get(session, url)
    if 'players' in resp:
        return resp['players']
    else:
        return None

