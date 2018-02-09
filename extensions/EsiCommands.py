from utils.importsfile import *
import utils.esiutils as esi


class EsiCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['co'])
    async def corp(self, ctx, *, corp: str):
        """ Displays public information about a corporation."""
        eid = await esi.get_id(corp, 'corp')
        if eid is None:
            return await ctx.send("Corp not found. Please Check your spelling and try again.")
        else:
            inf = await esi.esi_corp(eid)
            ceo = await esi.esi_char(inf['ceoid'])

            urls = {
                'zkb': f'https://zkillboard.com/corporation/{eid}/',
                'dotlan': f'https://evemaps.dotlan.net/corp/{eid}'
            }

            embed = discord.Embed(title=f'{inf["name"]} Corp Info', color=discord.Color.green())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url_as(format='png'))
            embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Corporation/{eid}_128.png')
            embed.add_field(name='Ticker', value=f'[{inf["ticker"]}]', inline=True)
            embed.add_field(name='Member Count', value=f'{inf["member"]}', inline=True)
            embed.add_field(name='CEO', value=f'{ceo["name"]}', inline=True)
            if inf['dob'] is not None:
                embed.add_field(name='Founded', value=inf["dob"].strftime("%a %d %b, %Y"), inline=True)
            if inf['ally'] is not None:
                ally = await esi.esi_ally(inf['ally'])
                embed.add_field(name='Alliance', value=f'{ally["name"]} [{ally["ticker"]}]', inline=False)
            embed.add_field(name='Additional Information', value=f'{urls["zkb"]}\n{urls["dotlan"]}', inline=False)

            return await ctx.send(embed=embed)

    @commands.command(aliases=['a'])
    async def ally(self, ctx, *, ally: str):
        """ Displays public information for an alliance."""
        eid = await esi.get_id(ally, 'ally')
        if eid is None:
            return await ctx.send('Alliance not found, please check your spelling and try again.')
        else:
            inf = await esi.esi_ally(eid)
            ecorp = await esi.esi_corp(inf['exec'])
            ccorp = await esi.esi_corp(inf['create_corp'])
            founder = await esi.esi_char(inf['founder'])

            urls = {
                'zkb': f'https://zkillboard.com/alliance/{eid}/',
                'dotlan': f'https://evemaps.dotlan.net/alliance/{eid}'
            }

            embed = discord.Embed(title=f'{inf["name"]} Alliance Info', color=discord.Color.blue())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url_as(format='png'))
            embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Alliance/{eid}_128.png')
            embed.add_field(name='Ticker', value=f'[{inf["ticker"]}]', inline=True)
            embed.add_field(name='Executor Corp', value=f'{ecorp["name"]} [{ecorp["ticker"]}]', inline=True)
            embed.add_field(name='Founder', value=f'{founder["name"]}', inline=True)
            embed.add_field(name='Founding Corp', value=f'{ccorp["name"]} [{ccorp["ticker"]}]', inline=True)
            embed.add_field(name='Founding Date', value=inf["founded"].strftime("%a %d %b, %Y"), inline=True)
            embed.add_field(name='Additional Information', value=f'{urls["zkb"]}\n{urls["dotlan"]}', inline=False)
            return await ctx.send(embed=embed)

    @commands.command(aliases=['ch'])
    async def char(self, ctx, *, char: str):
        """ Displays public information for a character. """
        eid = await esi.get_id(char, 'char')
        if eid is None:
            return await ctx.send('Character not found. please check your spelling and try again.')
        else:
            inf = await esi.esi_char(eid)
            corp = await esi.esi_corp(inf['corpid'])

            urln = urllib.parse.quote_plus(inf['name'])

            urls = {
                'zkb': f'https://zkillboard.com/character/{eid}/',
                'who': f'https://evehwo.com/pilot/{urln}'
            }

            embed = discord.Embed(title=f'{inf["name"]} Character Info')
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url_as(format='png'))
            embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Character/{eid}_128.jpg')
            embed.add_field(name='Corporation', value=f'{corp["name"]} [{corp["ticker"]}]', inline=True)
            if corp['ally'] is not None:
                ally = await esi.esi_ally(corp['ally'])
                embed.add_field(name='Alliance', value=f'{ally["name"]} [{ally["ticker"]}]')
            embed.add_field(name='Age', value=core.strftdelta(inf['age']), inline=True)
            embed.add_field(name='Birthday', value=inf["dob"].strftime("%a %d %b, %Y"), inline=True)
            embed.add_field(name='Additional Information', value=f'{urls["zkb"]}\n{urls["who"]}')

            return await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx):
        """ Displays the current status of Tranquility. """
        players = await esi.esi_status()
        if players is None:
            return await ctx.send("Tranquility is currently **OFFLINE**.")
        else:
            return await ctx.send(f'Tranquility is currently **ONLINE** with {str("{:,}".format(players))} players.')


def setup(killbot):
    killbot.add_cog(EsiCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(EsiCommands)
