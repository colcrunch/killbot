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

        embed = await kbutils.build_threat(stats, char, cid)

        return await ctx.send(embed=embed)


def setup(killbot):
    killbot.add_cog(kbCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(kbCommands)
