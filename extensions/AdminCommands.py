from utils.importsfile import *
from pathlib import Path as path
from bot import logger as logger
from utils.core import mc
import sqlite3


# noinspection PyUnusedLocal
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

    @commands.command(aliases=['ad'], hidden=True)
    @checks.guild_owner()
    async def admin(self, ctx, user: discord.Member):
        """ Promotes a user to admin permissions in the current guild. (Only bot owners can promote users to admins) """
        try:
            uid = user.id
            sid = ctx.guild.id
            core.promote(uid, sid)
            core.updateadmin(sid)
            logger.info(f'{ctx.author.name} promoted {user.name}{user.discriminator} to admin in {sid}.')
            return await ctx.send(f'{user.name}#{user.discriminator} has been promoted to an admin in this guild.')
        except sqlite3.IntegrityError:
            return await ctx.send(f'{user.name}#{user.discriminator} is already an admin in this guild.')

    @commands.command(aliases=['rad'], hidden=True)
    @checks.guild_owner()
    async def remove_admin(self, ctx, user: discord.Member):
        """ Demotes a member out of admin permissions in the current guild. (Owner Only)"""
        try:
            uid = user.id
            sid = ctx.guild.id
            core.demote(uid, sid)
            core.updateadmin(sid)
            return await ctx.send(f'{user.name}#{user.discriminator} has been demoted in this guild.')
        except sqlite3.IntegrityError:
            return await ctx.send(f'{user.name}#{user.discriminator} is not an admin in this guild.')

    @commands.command(aliases=['lad'], hidden=True)
    @checks.is_admin()
    async def list_admin(self, ctx):
        """ Lists all bot admins in the current guild. """
        admins = mc.get(f'{ctx.guild.id}_admin')
        if len(admins) is 0 or admins is None:
            return await ctx.send('There are no admins set for this guild yet.')
        adminis = []
        for admin in admins:
            admini = discord.Guild.get_member(ctx.guild, user_id=admin)
            if admini.nick is None:
                name = admini.name
            else:
                name = admini.nick
            adminis.append(f'{name} ({admini.name}#{admini.discriminator})')
        admins = "\n".join(adminis)
        return await ctx.send(f'```\n'
                              f'Admins: \n'
                              f'{admins}'
                              f'```')

    @commands.command(aliases=['cstats'], hidden=True)
    @checks.guild_owner()
    async def cache_stats(self, ctx):
        stat = mc.get_stats()
        stats = stat[0][1]
        maxmib = float(stats["limit_maxbytes"])/1048576
        msg = f'```' \
              f'Memcache Stats: \n-------------------\n' \
              f'Up Time (in seconds): {stats["uptime"]}\n' \
              f'Connections: Current: {stats["curr_connections"]} | Total: {stats["total_connections"]}\n' \
              f'Threads: {stats["threads"]}\n' \
              f'Max Size: {stats["limit_maxbytes"]} bytes | {str(maxmib)} MiB\n' \
              f'Total Size: {stats["bytes"]} bytes \n' \
              f'Cache Items: Current: {stats["curr_items"]} | Total: {stats["total_items"]}\n\n' \
              f'Hits and Misses:\n-------------------\n' \
              f'Get: {stats["get_hits"]} / {stats["get_misses"]}\n' \
              f'Del: {stats["delete_hits"]} / {stats["delete_misses"]}\n' \
              f'```'
        return await ctx.send(msg)

def setup(killbot):
    killbot.add_cog(AdminCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(AdminCommands)
