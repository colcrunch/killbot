from utils.importsfile import *
from pathlib import Path as path
from bot import logger as logger


class AdminCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ping(self, ctx):
        return await ctx.send('PONG!')

    @commands.command(aliases=['ul'], hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, ext):
        """ Unload an extension. """
        print(f'{ctx.author.name} unloading {ext}')
        try:
            check = path(f'extensions/{ext}.py')
            if not check.exists() or ext == 'AdminCommands':
                return await ctx.send(f'{ext} is not a valid extension.')
            self.bot.unload_extension(f'extensions.{ext}')
            logger.warning(f'{ext} Unloaded by {ctx.author.name}')
            print(f'{ext} Unloaded')
            return await ctx.send(f'{ext} Unloaded')
        except Exception as e:
            logger.error(f'Error unloading {ext}. Error: {e}')
            logger.error(traceback.print_exc())
            return print(e)

    @commands.command(aliases=['l'], hidden=True)
    @commands.is_owner()
    async def load(self, ctx, ext):
        """Load an Extension. """
        print(f'{ctx.author.name} loading {ext}')
        try:
            check = path(f'extensions/{ext}.py')
            if not check.exists() or ext == 'AdminCommands':
                return await ctx.send(f'{ext} is not a valid extension.')
            self.bot.load_extension(f'extensions.{ext}')
            logger.warning(f'{ext} Loaded by {ctx.author.name}')
            print(f'{ext} Loaded')
            return await ctx.send(f'{ext} Loaded')
        except Exception as e:
            logger.error(f'Error loading {ext}. Error: {e}')
            logger.error(traceback.print_exc())
            return print(e)

    @commands.command(aliases=['rl'], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, ext):
        """ Reload an extension. """
        print(f'{ctx.author.name} reloading {ext}')
        try:
            check = path(f'extensions/{ext}.py')
            if not check.exists():
                return await ctx.send(f'{ext} is not a valid extension')
            self.bot.unload_extension(f'extensions.{ext}')
            print(f'{ext} Unloaded')
            self.bot.load_extension(f'extensions.{ext}')
            print(f'{ext} Loaded')
            logger.warning(f'{ext} Reloaded by {ctx.author.name}')
            return await ctx.send(f'{ext} Reloaded')
        except Exception as e:
            logger.error(f'Error reloading {ext}. Error: {e}')
            logger.error(traceback.print_exc())
            print(e)

    @commands.command(aliases=['pr'], hidden=True)
    @commands.is_owner()
    async def presence(self, ctx, state, *, pres: str):
        """ Sets bot presence. """
        statuses = {'online': discord.Status.online,
                    'dnd': discord.Status.dnd,
                    'idle': discord.Status.idle,
                    'offline': discord.Status.offline,
                    'invisible': discord.Status.invisible}

        game = discord.Game(name=pres)
        if state in statuses:
            status = statuses[state]
            return await self.bot.change_presence(status=status, activity=game)
        elif state not in statuses or state is None:
            return await self.bot.change_presence(activity=game)

    @commands.command(aliases=['ld'], hidden=True)
    @commands.is_owner()
    async def loaded(self, ctx):
        exts = '\n'.join(list(self.bot.extensions))
        cogs = '\n'.join(list(self.bot.cogs))

        ext_num = len(self.bot.extensions)
        cog_num = len(self.bot.cogs)

        return await ctx.send(f'```\n'
                              f'Extensions: {ext_num} Extensions Loaded with {cog_num} Cogs \n\n{exts} \n\n'
                              f'Cogs: {cog_num} Loaded \n\n{cogs}'
                              f'```')


def setup(killbot):
    killbot.add_cog(AdminCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(AdminCommands)
