from utils.importsfile import *
import utils.marketutils as market
from utils.config import prefix as prefix
from utils.core import mc


class MarketCommands:
    def __init__(self, bot):
        self.bot = bot
        self.prefix = bot.prefix
        self.logger = self.bot.logger

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
                # If we have to hit ESI for a type_id, this means that the SDE that is currently in use is likely old.
                if mc.get('sde_update_notice') is None:
                    self.logger.warning("It appears that the SDE may be out of date. Please run the launcher update"
                                        " command")
                    appinf = await self.bot.application_info()
                    owner = self.bot.get_user(appinf.owner.id)
                    await owner.send("It appears the SDE is out of date, please run `python3 launcher.py update` and "
                                     "restart the bot.")
                    # Notifications should only happen once a day.
                    mc.set('sde_update_notice', True, 86400)

                item = await esiutils.esi_type(item_id)
        else:
            item = sdeutils.type_name(item_id)

        info = await market.get_price(item_id, region_id)

        embed = await market.build(info, item, item_id, region)

        return await ctx.send(embed=embed)

    @commands.group(aliases=['pc'])
    async def price_check(self, ctx, *item):
        """ Checks prices for specified items in a specified region. (Default: The Forge) """
        item = list(item)
        # noinspection PyShadowingNames
        prefix = self.prefix
        if prefix+'r' in item:
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

    # noinspection PyUnusedLocal
    @price_check.command(name=f'{prefix}r')
    async def placeholder(self, ctx):
        """ Use this to select the region to use in a price check. """
        # This function should never get called!
        return False


def setup(killbot):
    killbot.add_cog(MarketCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(MarketCommands)