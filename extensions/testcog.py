from utils.importsfile import *

class TestCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ping(self, ctx):
        return await ctx.send('PONG!')


def setup(killbot):
    killbot.add_cog(TestCommands(killbot))