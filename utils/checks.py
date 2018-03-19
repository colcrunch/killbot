from utils.importsfile import *
from utils.core import mc

def is_admin():
    """ Checks if a user is on the list of admins for a guild. """
    async def predicate(ctx):
        if await ctx.bot.is_owner(ctx.author):
            return True
        sid = ctx.guild.id
        user = ctx.author.id
        admins = mc.get(f'{sid}_admin')
        return user in admins

    return commands.check(predicate)