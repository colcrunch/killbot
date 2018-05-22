from utils.importsfile import *


class BotCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
        """Displays general information about the bot."""
        info = await self.bot.application_info()
        owner = "{0}#{1}".format(info.owner.name, info.owner.discriminator)
        link = "https://github.com/colcrunch/killbot"
        about = ("Killbot is a general use discord bot for use with EVE Online."
                 "The aim of Killbot is to make it easy to get public info from the game and"
                 "to easily monitor zkillboard for kills that are interesting to you.")

        embed = discord.Embed(title="About {}".format(self.bot.user.name), description=about)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.set_thumbnail(url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name="Bot Owner", value=owner, inline=True)
        embed.add_field(name="Bot Author", value="col_crunch#2370", inline=True)
        embed.add_field(name="GitHub", value=link, inline=False)

        return await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        """ Displpays various statistics about the bot"""
        servers = []
        for guild in self.bot.guilds:
            servers.append(guild)

        now = datetime.datetime.utcnow()

        uptime = now - self.bot.start_time

        embed = discord.Embed(title="Bot Statistics", colour=discord.Colour.green())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.set_thumbnail(url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name="Servers", value=str(len(servers)), inline=True)
        embed.add_field(name="Uptime", value=core.strftdelta(uptime), inline=True)
        if 'WatchRedisq' in self.bot.cogs:
            embed.add_field(name="Killmails Processed", value=self.bot.counter, inline=True)
            embed.add_field(name="Posted",
                            value="**Kills:** {0} \n**Losses:** {1} \n**Total:** {2}".format(self.bot.kcounter, self.bot.lcounter,
                                                                                             (self.bot.kcounter + self.bot.lcounter)),
                            inline=True)

        return await ctx.send(embed=embed)

    @commands.command(aliases=['et'])
    async def evetime(self, ctx):
        """ Returns the current EVE (UTC) time. """
        return await ctx.send(f'The current EVE (UTC) time is: **{datetime.datetime.utcnow().strftime("%H:%M")}**')


def setup(killbot):
    killbot.add_cog(BotCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(BotCommands)