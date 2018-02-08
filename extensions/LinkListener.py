from utils.importsfile import *
import re
from utils import marketutils, kbutils

class LinkListener:
    def __init__(self, bot):
        self.bot = bot

    def passed(self, check):
        message = msg
        return check.id == message.id

    async def on_message(self, message):
        match = re.match(r'(.*)(http[s]?://([A-Za-z]*).[a-zA-z]*(/[a-zA-z]*/?)([0-9]*)[a-zA-Z/]?)', message.content)
        """
         Match Groups:
         Group 1 (match[1]): anything preceding the link.
         Group 2 (match[2]): The link in its entirety
         Group 3 (match[3]): The domain of the URL. This is how we determine if/how to process it.
         Group 4 (match[4]): Only used for zkill at the moment, to determine if the URL is a kill or not.
         Group 5 (match[5]): The ID we will need for processing. We know that all the services we want to process use 
                             only numeric IDs, so this is fine. (Though probably not the best if we wanted to add 
                             dscan.me support or something.
        """
        channel = message.channel
        global msg
        msg = message
        if match and (message.author != self.bot.user):
            if match[3] == 'evemarketer':
                typeid = match[5]
                item = sdeutils.type_name(typeid)
                info = await marketutils.get_price(typeid, None)
                content = f'{message.author.mention} shared {message.content}'

                embed = discord.Embed(title=f'{item} Market Information')
                embed.set_author(name='EveMarketer', icon_url='https://evemarketer.com/static/img/logo_32.png',
                                 url=f'https://evemarketer.com/types/{typeid}')
                embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Type/{typeid}_64.png')
                embed.add_field(name="Sell Min", value=info['sMin'], inline=True)
                embed.add_field(name="Sell Max", value=info['sMax'], inline=True)
                if item.lower() == 'plex':
                    embed.add_field(name='Sell Avg', value=info['sAvg'], inline=True)
                    embed.add_field(name='Monthly Sub Sell Avg', value='{:,}'.format(round(info['plex'][0] * 500, 2)),
                                    inline=True)
                else:
                    embed.add_field(name='Sell Avg', value=info['sAvg'], inline=False)
                embed.add_field(name='Buy Min', value=info['bMin'], inline=True)
                embed.add_field(name='Buy Max', value=info['bMax'], inline=True)
                if item.lower() == 'plex':
                    embed.add_field(name='Buy Avg', value=info['bAvg'], inline=True)
                    embed.add_field(name='Monthly Sub Buy Avg', value='{:,}'.format(round(info['plex'][1] * 500, 2)),
                                    inline=True)
                else:
                    embed.add_field(name='Buy Avg', value=info['bAvg'], inline=True)
                if match[1] is not '':
                    return await channel.send(embed=embed)
                else:
                    await channel.purge(check=self.passed)

                    return await channel.send(content=content, embed=embed)
            elif match[3] == 'zkillboard':
                if match[4] == '/kill/':
                    killid = match[5]
                    km = await kbutils.get_mail(killid)
                    content = f'{message.author.mention} shared {message.content}'

                    vic = km['victim']
                    if 'character_id' not in vic:
                        vicChar = None
                    else:
                        vicChar = await esiutils.esi_char(vic['character_id'])
                    vicShip = sdeutils.type_name(vic['ship_type_id'])
                    vicCorp = await esiutils.esi_corp(vic['corporation_id'])
                    if 'alliance_id' in vic:
                        vicAlly = await esiutils.esi_ally(vic['alliance_id'])
                    else:
                        vicAlly = None
                    vicDam = '{:,}'.format(vic['damage_taken'])
                    loc = sdeutils.system_name(km['location'])
                    for attacker in km['attackers']:
                        if attacker['final_blow'] is True:
                            attChar = await esiutils.esi_char(attacker['character_id'])
                            attCorp = await esiutils.esi_corp(attacker['corporation_id'])
                            if 'alliance_id' in attacker:
                                attAlly = await esiutils.esi_ally(attacker['alliance_id'])
                            else:
                                attAlly = None
                            attShip = sdeutils.type_name(attacker['ship_type_id'])

                    if vicChar is None:
                        if vicAlly is None:
                            embed = discord.Embed(title=f'{vicCorp["name"]} lost their {vicShip}')
                        else:
                            embed = discord.Embed(title=f'{vicCorp["name"]} ({vicAlly["name"]}) lost their {vicShip}')
                    else:
                        embed = discord.Embed(title=f'{vicChar["name"]} ({vicCorp["name"]}) lost their {vicShip}',
                                          timestamp=km['time'])
                    embed.set_author(name='zKillboard', icon_url='https://zkillboard.com/img/wreck.png',
                                     url=f'http://zkillboard.com/kill/{killid}/')
                    embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Type/{vic["ship_type_id"]}_64.png')
                    embed.add_field(name='Final Blow', value=attChar['name'], inline=True)
                    if attAlly is None:
                        embed.add_field(name='Corp', value=f'{attCorp["name"]}', inline=True)
                    else:
                        embed.add_field(name='Corp', value=f'{attCorp["name"]}({attAlly["name"]})', inline=True)
                    embed.add_field(name='Value', value=f'{km["value"]} ISK', inline=True)
                    embed.add_field(name='Damage Taken', value=vicDam, inline=True)
                    embed.add_field(name='System', value=loc, inline=False)

                    if match[1] is not '':
                        return await channel.send(embed=embed)
                    else:
                        await channel.purge(check=self.passed)

                        return await channel.send(content=content, embed=embed)

        else:
            return


def setup(killbot):
    killbot.add_cog(LinkListener(killbot))


def teardown(killbot):
    killbot.remove_cog(LinkListener)