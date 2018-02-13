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
            else:
                item = esiutils.esi_type(item_id)
        else:
            item = sdeutils.type_name(item_id)

        info = await market.get_price(item_id, region_id)

        embed = await market.build(info, item, item_id, region)

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