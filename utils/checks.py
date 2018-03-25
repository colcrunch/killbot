from utils.importsfile import *
from utils.core import mc

def is_admin():
    """ Checks if a user is on the list of admins for a guild. """
    async def predicate(ctx):
        if type(ctx.channel) is discord.DMChannel:
            return False
        if await ctx.bot.is_owner(ctx.author):
            return True
        elif ctx.author is ctx.guild.owner:
            return True
        sid = ctx.guild.id
        user = ctx.author.id
        admins = mc.get(f'{sid}_admin')
        return user in admins

    return commands.check(predicate)

def guild_owner():
    """ Checks if a user is the owner of the guild. """
    async def predicate(ctx):
        if type(ctx.channel) is discord.DMChannel:
            return False
        if await ctx.bot.is_owner(ctx.author):
            return True
        if ctx.author is ctx.guild.owner:
            return True

    return commands.check(predicate)

