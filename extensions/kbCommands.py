from utils.importsfile import *
from utils import kbutils

# TODO: Logging


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

        # If the character is too new/has no kills or losses, we wont be able to get much useful info from the api.
        if all(value is None for value in stats.values()):
            if 'extensions.EsiCommands' in self.bot.extensions:
                return await ctx.send(f'This character has no killboard stats. Please use the `{config.prefix}char '
                                      f'command` to display information on this character.')
            else:
                return await ctx.send('This character has no killboard stats.')

        embed = await kbutils.build_threat(stats, char, cid)

        return await ctx.send(embed=embed)


def setup(killbot):
    killbot.add_cog(kbCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(kbCommands)
