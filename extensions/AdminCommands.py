from utils.importsfile import *
from pathlib import Path as path

class AdminCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ping(self, ctx):
        return await ctx.send('PONG!')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, ext):
        """ Unload an extension. """
        # TODO: Log this stuff
        print('{0} unloading {1}'.format(ctx.author.name, ext))
        try:
            check = path('extensions/{}.py'.format(ext))
            if not check.exists():
                return await ctx.send('{} is not a valid extension.'.format(ext))
            self.bot.unload_extension(ext)
            print('{} Unloaded'.format(ext))
            return await ctx.send('{} Unloaded'.format(ext))
        except Exception as e:
            return print(e)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, ext):
        """Load an Extension. """
        # TODO: Log this stuff.
        print('{0} loading {1}'.format(ctx.author.name, ext))
        try:
            check = path('extensions/{}.py'.format(ext))
            if not check.exists():
                return await ctx.send('{} is not a valid extension.'.format(ext))
            self.bot.unload_extension(ext)
            print('{} Loaded'.format(ext))
            return await ctx.send('{} Loaded'.format(ext))
        except Exception as e:
            return print(e)


def setup(killbot):
    killbot.add_cog(AdminCommands(killbot))