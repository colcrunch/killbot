from utils.importsfile import *
import re
from utils import marketutils

class LinkListener:
    def __init__(self, bot):
        self.bot = bot

    def passed(self, check):
        message = msg
        return check.id == message.id

    async def on_message(self, message):
        match = re.match(r'http[s]?://([A-Za-z]*).[a-zA-z/]*([0-9]*)[a-zA-Z/]?', message.content)
        channel = message.channel
        global msg
        msg = message
        if match:
            if match[1] == 'evemarketer':
                typeid = match[2]
                item = sdeutils.type_name(typeid)
                info = await marketutils.get_price(typeid, None)
                content = f'{message.author.mention} shared {message.content}'

                embed = discord.Embed(title=f'{item} Market Information')
                embed.set_author(name='EveMarketer', icon_url='https://evemarketer.com/static/img/logo_32.png',
                                 url=f'https://evemarketer.com/types/{typeid}')
                embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Type/{typeid}_64.png')
                embed.add_field(name="Sell Min", value=info['sMin'], inline=True)
                embed.add_field(name="Sell Max", value=info['sMax'], inline=True)
                if item.lower() == 'plex':
                    embed.add_field(name='Sell Avg', value=info['sAvg'], inline=True)
                    embed.add_field(name='Monthly Sub Sell Avg', value='{:,}'.format(round(info['plex'][0] * 500, 2)),
                                    inline=True)
                else:
                    embed.add_field(name='Sell Avg', value=info['sAvg'], inline=False)
                embed.add_field(name='Buy Min', value=info['bMin'], inline=True)
                embed.add_field(name='Buy Max', value=info['bMax'], inline=True)
                if item.lower() == 'plex':
                    embed.add_field(name='Buy Avg', value=info['bAvg'], inline=True)
                    embed.add_field(name='Monthly Sub Buy Avg', value='{:,}'.format(round(info['plex'][1] * 500, 2)),
                                    inline=True)
                else:
                    embed.add_field(name='Sell Avg', value=info['bAvg'], inline=True)

                await channel.purge(check=self.passed)

                return await channel.send(content=content, embed=embed)
            else:
                return

        else:
            return


def setup(killbot):
    killbot.add_cog(LinkListener(killbot))


def teardown(killbot):
    killbot.remove_cog(LinkListener)