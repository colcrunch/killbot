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
            if 'shipsDestroyed' in months[month]:
                kMonth = months[month]['shipsDestroyed']
            else:
                kMonth = 0
            if 'shipsLost' in months[month]:
                lMonth = months[month]['shipsLost']
            else:
                lMonth = 0
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


async def build_kill(km, type):

    if type == 'api':
        vicChar = km['vicChar']
        vicAlly = km['vicAlly']
        vicCorp = km['vicCorp']
        vicShip = km['vicShip']
        vicST = km['vicST']
        killid = km['kid']
        loc = km['loc']
        attChar = km['attChar']
        attCorp = km['attCorp']
        attAlly = km['attAlly']
        vicDam = km['vicDam']
        value = km['value']
        killTime = km['time']
    elif type == 'esi':
        vic = km['killmail']['victim']
        if 'character_id' in vic:
            vicChar = await esiutils.esi_char(vic['character_id'])
        else:
            vicChar = None
        if 'corporation_id' in vic:
            vicCorp = await esiutils.esi_corp(vic['corporation_id'])
        else:
            vicCorp = None
        if 'alliance_id' in vic:
            vicAlly = await esiutils.esi_ally(vic['alliance_id'])
        else:
            vicAlly = None
        vicDam = '{:,}'.format(vic['damage_taken'])
        vicST = vic['ship_type_id']
        vicShip = sdeutils.type_name(vicST)
        attackers = km['killmail']['attackers']
        for attacker in attackers:
            if attacker['final_blow'] is True:
                if 'character_id' in attacker:
                    attChar = await esiutils.esi_char(attacker['character_id'])
                else:
                    attChar = None
                attCorp = await esiutils.esi_corp(attacker['corporation_id'])
                if 'alliance_id' in attacker:
                    attAlly = await esiutils.esi_ally(attacker['alliance_id'])
                else:
                    attAlly = None
                attShip = sdeutils.type_name(attacker['ship_type_id'])
        loc = sdeutils.system_name(km['killmail']['solar_system_id'])
        value = '{:,}'.format(km['zkb']['totalValue'])
        killid = km['killID']
        killTime = datetime.datetime.strptime(km['killmail']['killmail_time'], '%Y-%m-%dT%H:%M:%SZ')


    if vicChar is None:
        if vicAlly is None:
            embed = discord.Embed(title=f'{vicCorp["name"]} lost their {vicShip}', timestamp=killTime)
        else:
            embed = discord.Embed(title=f'{vicCorp["name"]} ({vicAlly["name"]}) lost their {vicShip}', timestamp=killTime)
    else:
        embed = discord.Embed(title=f'{vicChar["name"]} ({vicCorp["name"]}) lost their {vicShip}',
                              timestamp=killTime)
    embed.set_author(name='zKillboard', icon_url='https://zkillboard.com/img/wreck.png',
                     url=f'http://zkillboard.com/kill/{killid}/')
    embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Type/{vicST}_64.png')
    if attChar is not None:
        embed.add_field(name='Final Blow', value=attChar['name'], inline=True)
    else:
        embed.add_field(name='Final Blow', value=attShip, inline=True)
    if attAlly is None:
        embed.add_field(name='Corp', value=f'{attCorp["name"]}', inline=True)
    else:
        embed.add_field(name='Corp', value=f'{attCorp["name"]}({attAlly["name"]})', inline=True)
    embed.add_field(name='Value', value=f'{value} ISK', inline=True)
    embed.add_field(name='Damage Taken', value=vicDam, inline=True)
    embed.add_field(name='System', value=loc, inline=False)

    return embed


async def build_threat(stats, char, cid):
    kdrAll = round(stats['kills'] / stats['losses'], 2)
    if stats['month'] is not None:
        kdrMonth = round(stats['month']['kills'] / stats['month']['losses'], 2)
    iskEff = round((1.0 - (stats['iskLost'] / stats['iskDestroyed'])) * 100, 1)
    iskD = '{:,}'.format(stats['iskDestroyed'])
    iskL = '{:,}'.format(stats['iskLost'])

    embed = discord.Embed(title=f'{char["name"]} Threat Analysis')
    embed.set_author(name='zKillboard', url=f'http://zkillboard.com/character/{cid}/',
                     icon_url='http://zkillboard.com/img/wreck.png')
    embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Character/{cid}_128.jpg')
    embed.add_field(name='Gang Ratio', value=f'{stats["gangRatio"]}%')
    embed.add_field(name='Danger Ratio', value=f'{stats["dangerRatio"]}%')
    embed.add_field(name='KDR All Time', value=f'Kills: {stats["kills"]} \nLosses: {stats["losses"]} \n'
                                               f'KDR: {kdrAll}')
    if stats['month'] is not None:
        embed.add_field(name='KDR Month', value=f'Kills: {stats["month"]["kills"]} \n'
                                                f'Losses: {stats["month"]["losses"]} \nKDR: {kdrMonth}')
    else:
        embed.add_field(name='KDR Month', value='No Kills Yet')
    embed.add_field(name='ISK Efficiency', value=f'ISK Killed: {iskD} \nISK Lost: {iskL} \nEfficiency: {iskEff}%')

    return embed
