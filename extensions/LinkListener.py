from utils.importsfile import *
import re
from utils import marketutils, kbutils
from sqlite3 import IntegrityError
from utils.core import mc


class LinkListener:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ig'], hidden=True)
    @checks.is_admin()
    async def ignore(self, ctx, channel: discord.TextChannel):
        """ Tells LinkListener to ignore a channel. """
        try:
            chid = channel.id
            print(chid)
            core.link_ignore(chid, ctx.guild.id)
            core.load_ignore(ctx.guild.id)
            return await ctx.send(f'Channel ignored.')
        except IntegrityError:
            return await ctx.send(f'Channel already ignored.')

    @commands.command(aliases=['uig'], hidden=True)
    @checks.is_admin()
    async def unignore(self, ctx, channel: discord.TextChannel):
        """ Tells LinkListener to stop ignoring a channel. """
        try:
            chid = channel.id
            core.stop_ignore(chid, ctx.guild.id)
            core.load_ignore(ctx.guild.id)
            return await ctx.send(f'Listening to channel again.')
        except IntegrityError:
            return await ctx.send(f'Channel not being ignored.')

    @staticmethod
    def passed(check):
        message = msg
        return check.id == message.id

    async def on_message(self, message):
        chid = message.channel.id
        if type(message.channel) is discord.TextChannel:
            ignore = mc.get(f'{message.guild.id}_dontListen')
        else:
            ignore = []
        if chid in ignore:
            print("test")
            return
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

                embed = await marketutils.build(info, item, typeid, None)

                if match[1] is not '':
                    return await channel.send(embed=embed)
                else:
                    if commands.bot_has_permissions(manage_messages=True):
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
                            if 'character_id' in attacker:
                                attChar = await esiutils.esi_char(attacker['character_id'])
                            else:
                                attChar = None
                            attCorp = await esiutils.esi_corp(attacker['corporation_id'])
                            if 'alliance_id' in attacker:
                                attAlly = await esiutils.esi_ally(attacker['alliance_id'])
                            else:
                                attAlly = None
                            # noinspection PyUnusedLocal
                            attShip = sdeutils.type_name(attacker['ship_type_id'])

                    # noinspection PyUnboundLocalVariable,PyUnboundLocalVariable,PyUnboundLocalVariable
                    dict_km = {'vicChar': vicChar,
                               'vicShip': vicShip,
                               'vicCorp': vicCorp,
                               'vicAlly': vicAlly,
                               'vicDam': vicDam,
                               'time': km['time'],
                               'vicST': vic['ship_type_id'],
                               'attChar': attChar,
                               'attCorp': attCorp,
                               'attAlly': attAlly,
                               'value': km['value'],
                               'loc': loc,
                               'kid': killid}

                    embed = await kbutils.build_kill(dict_km, 'api')

                    if match[1] is not '':
                        return await channel.send(embed=embed)
                    else:
                        if commands.bot_has_permissions(manage_messages=True):
                            await channel.purge(check=self.passed)

                        return await channel.send(content=content, embed=embed)
                elif match[4] == '/character/':
                    cid = match[5]
                    char = await esiutils.esi_char(cid)

                    stats = await kbutils.get_stats(cid)

                    if all(value is None for value in stats.values()):
                        if 'extensions.EsiCommands' in self.bot.extensions:
                            return await channel.send(
                                f'This character has no killboard stats. Please use the `{config.prefix}char '
                                f'command` to display information on this character.')
                        else:
                            return await channel.send('This character has no killboard stats.')

                    embed = await kbutils.build_threat(stats, char, cid)

                    return await channel.send(embed=embed)

        else:
            return


def setup(killbot):
    killbot.add_cog(LinkListener(killbot))


def teardown(killbot):
    killbot.remove_cog(LinkListener)