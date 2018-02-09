from utils.importsfile import *
from utils import kbutils


class kbCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['t'])
    async def threat(self, ctx, *, char: str):
        """ Returns info on a character from the zKill stats API. """
        cid = await esiutils.get_id(char, 'char')
        if cid is None:
            return await ctx.send('Character not found. Please check your spelling and try again.')
        char = await esiutils.esi_char(cid)

        stats = await kbutils.get_stats(cid)

        kdrAll = round(stats['kills']/stats['losses'],2)
        if stats['month'] is not None:
            kdrMonth = round(stats['month']['kills']/stats['month']['losses'],2)
        iskEff = round((1.0 - (stats['iskLost']/stats['iskDestroyed']))*100, 1)
        iskD = '{:,}'.format(stats['iskDestroyed'])
        iskL = '{:,}'.format(stats['iskLost'])

        # If the character is too new/has no kills or losses, we wont be able to get much useful info from the api.
        if all(value is None for value in stats.values()):
            if 'extensions.EsiCommands' in self.bot.extensions:
                return await ctx.send(f'This character has no killboard stats. Please use the `{config.prefix}char '
                                      f'command` to display information on this character.')
            else:
                return await ctx.send('This character has no killboard stats.')

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

        return await ctx.send(embed=embed)


def setup(killbot):
    killbot.add_cog(kbCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(kbCommands)
