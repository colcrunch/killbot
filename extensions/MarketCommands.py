from utils.importsfile import *
import utils.marketutils as market
from utils.config import prefix as prefix

class MarketCommands:
    def __init__(self, bot):
        self.bot = bot
        self.prefix = bot.prefix

    async def process_item(self, ctx, item, region):
        region_id = sdeutils.region_id(region)
        item_id = sdeutils.type_id(item)

        if region_id is None:
            region_id = await esiutils.get_id(region, 'region')
            if region_id is None:
                return await ctx.send('Region not found.')
        if item_id is None:
            item_id = await esiutils.get_id(item, 'itype')
            if item_id is None:
                return await ctx.send('Item not found.')

        info = await market.get_price(item_id, region_id)

        embed = discord.Embed(title=f'{item} - {region} Market Information')
        embed.set_author(name='EveMarketer', icon_url='https://evemarketer.com/static/img/logo_32.png',
                         url=f'https://evemarketer.com/types/{item_id}')
        embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Type/{item_id}_64.png')
        embed.add_field(name="Sell Min", value=info['sMin'], inline=True)
        embed.add_field(name="Sell Max", value=info['sMax'], inline=True)
        if item.lower() == 'plex':
            embed.add_field(name='Sell Avg', value=info['sAvg'], inline=True)
            embed.add_field(name='Monthly Sub Sell Avg', value='{:,}'.format(round(info['plex'][0]*500, 2)), inline=True)
        else:
            embed.add_field(name='Sell Avg', value=info['sAvg'], inline=False)
        embed.add_field(name='Buy Min', value=info['bMin'], inline=True)
        embed.add_field(name='Buy Max', value=info['bMax'], inline=True)
        if item.lower() == 'plex':
            embed.add_field(name='Buy Avg', value=info['bAvg'], inline=True)
            embed.add_field(name='Monthly Sub Buy Avg', value='{:,}'.format(round(info['plex'][1]*500, 2)), inline=True)
        else:
            embed.add_field(name='Sell Avg', value=info['bAvg'], inline=True)

        return await ctx.send(embed=embed)

    @commands.group(aliases=['pc'])
    async def price_check(self, ctx, *item):
        """ Checks prices for specified items in a specified region. (Default: The Forge) """
        item = list(item)
        prefix = self.prefix
        if self.prefix+'r' in item:
            i = item.index(prefix + 'r')
            item_list = item[:i]
            region_list = item[i + 1:]
            item = " ".join(item_list)
            region_name = " ".join(region_list)
            return await self.process_item(ctx, item, region_name)
        else:
            region_name = 'The Forge'
            it = " ".join(item)
            item = it
            return await self.process_item(ctx, item, region_name)

    @price_check.command(name=f'{prefix}r')
    async def placeholder(self, ctx):
        """ Use this to select the region to use in a price check. """
        # This function should never get called!
        return False


def setup(killbot):
    killbot.add_cog(MarketCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(MarketCommands)