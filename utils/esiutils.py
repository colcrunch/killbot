from utils.importsfile import *
from utils.core import get_esi as get
from utils.core import mc


async def get_id(name, ref):
    key_name = name.replace(' ', '+')
    if mc.get(f'{ref}_{key_name}') is None:
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
            respo = await get(session, url)
        resp = respo['resp']
        exp = respo['exp']
        if defs[ref] in resp:
            eid = str(resp[defs[ref]][0])
        else:
            eid = None
        mc.set(f'{ref}_{key_name}', f'{eid}', exp.seconds)
        return eid
    else:
        print(f'Getting id for {name} from cache.')
        return mc.get(f'{ref}_{key_name}')


async def esi_char(eid):
    if mc.get(f'{eid}') is None:
        url = f'https://esi.tech.ccp.is/v4/characters/{eid}/?datasource=tranquility'
        async with aiohttp.ClientSession() as session:
            respo = await get(session, url)
        resp = respo['resp']
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
        mc.set(f'{eid}', inf, respo['exp'].seconds)
        return inf
    else:
        print(f'Getting char info for {eid} from cache.')
        return mc.get(f'{eid}')


async def esi_corp(eid):
    if mc.get(f'{eid}') is None:
        url = f'https://esi.tech.ccp.is/v4/corporations/{eid}/?datasource=tranquility'
        async with aiohttp.ClientSession() as session:
            respo = await get(session, url)
        resp = respo['resp']
        exp = respo['exp']
        name = resp['name']
        ticker = resp['ticker']
        member = resp['member_count']
        ceoid = resp['ceo_id']
        if 'alliance_id' in resp:
            ally = resp['alliance_id']
        else:
            ally = None
        if 'date_founded' in resp:
            dob = datetime.datetime.strptime(resp['date_founded'], '%Y-%m-%dT%H:%M:%SZ')
        else:
            dob = None
        if 'url' not in resp or resp['url'] == 'http://' or resp['url'] == '' or resp['url'] == 'https://':
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
        mc.set(f'{eid}', inf, exp.seconds)
        sanitized_ticker = ticker.replace(" ", "+")
        mc.set(f'corp_{sanitized_ticker}', eid, exp.seconds)
        name = name.replace(' ','')
        mc.set(f'corp_{name}', eid, exp.seconds)
        return inf
    else:
        print(f'Getting corp info for {eid} from cache.')
        return mc.get(f'{eid}')


async def esi_ally(eid):
    if mc.get(f'{eid}') is None:
        url = f'https://esi.tech.ccp.is/v3/alliances/{eid}/?datasource=tranquility'
        async with aiohttp.ClientSession() as session:
            respo = await get(session, url)
        resp = respo['resp']
        exp = respo['exp']
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
        mc.set(f'{eid}', inf, exp.seconds)
        mc.set(f'ally_{ticker}', eid, exp.seconds)
        name = name.replace(' ','')
        mc.set(f'ally_{name}', eid, exp.seconds)
        return inf
    else:
        print(f'Getting alliance info for {eid} from cache.')
        return mc.get(f'{eid}')


async def esi_type(eid):
    ed = f'{eid}'
    if mc.get(ed) is None:
        url = f'http://esi.tech.ccp.is/v3/universe/types/{eid}/?datasource=tranquility'
        async with aiohttp.ClientSession() as session:
            respo = await core.get_esi(session, url)
        resp = respo['resp']
        exp = respo['exp']
        if 'name' in resp:
            name = resp['name']
        else:
            name = None
        mc.set(ed, name, exp.seconds)
        return name
    else:
        print(f'Getting type info for {ed} from cache.')
        return mc.get(ed)


async def esi_system(eid):
    if mc.get(f'{eid}') is None:
        url = f'https://esi.tech.ccp.is/v3/universe/systems/{eid}/?datasource=tranquility'
        async with aiohttp.ClientSession() as session:
            respo = await get(session, url)
        resp = respo['resp']
        exp = respo['exp']

        name = resp['name']
        star = resp['star_id']
        sec = round(resp['security_status'], 2)
        constellation = resp['constellation_id']
        planets = len(resp['planets'])
        listlen = []
        for planet in resp['planets']:
            if 'moons' in planet:
                listlen.append(len(planet['moons']))

        moons = sum(listlen)
        secClass = resp['security_class']
        gates = len(resp['stargates'])
        if 'stations' in resp:
            stations = len(resp['stations'])
        else:
            stations = None

        inf = {'name': name,
               'star': star,
               'sec': sec,
               'secClass': secClass,
               'const': constellation,
               'planets': planets,
               'moons': moons,
               'gates': gates,
               'stations': stations}
        mc.set(f'{eid}', inf, exp.seconds)
        return inf
    else:
        print(f"Getting system information for {eid} from cache.")
        return mc.get(f'{eid}')


async def esi_sysKills():
    if mc.get('sysKills') is None:
        url = 'https://esi.tech.ccp.is/v2/universe/system_kills/'
        async with aiohttp.ClientSession() as session:
            respo = await get(session, url)
        resp = respo['resp']
        exp = respo['exp']
        mc.set('sysKills', resp, exp.seconds)
        return resp
    else:
        print("Getting system kill information from cache.")
        return mc.get('sysKills')


async def esi_sysJumps():
    if mc.get('sysJumps') is None:
        url = 'https://esi.tech.ccp.is/v1/universe/system_jumps/'
        async with aiohttp.ClientSession() as session:
            respo = await get(session, url)
        resp = respo['resp']
        exp = respo['exp']
        mc.set('sysJumps', resp, exp.seconds)
        return resp
    else:
        print("Getting system jump information from cache.")
        return mc.get('sysJumps')


async def esi_status():
    if mc.get('status') is None:
        url = "https://esi.tech.ccp.is/latest/status/?datasource=tranquility"
        async with aiohttp.ClientSession() as session:
            respo = await get(session, url)
        if respo['code'] is not 200:
            return None
        resp = respo['resp']
        exp = respo['exp']
        print(exp)
        if 'players' in resp:
            mc.set('status', resp['players'], exp.seconds)
            return resp['players']
        else:
            return None
    else:
        print('Getting status from cache')
        return mc.get('status')

