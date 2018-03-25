from utils.importsfile import *
from utils.core import get_json as get
from utils.core import mc


class TheraWatch:
    def __init__(self, bot):
        self.bot = bot
        self.regions = config.regions
        self.cons = config.cons
        self.systems = config.systems
        self.channel = self.bot.get_channel(config.thera_channel)

        self.bg_task = self.bot.loop.create_task(self.thera())

    async def post(self, level, info):
        tid = info['id']
        mc.set(f'last_thera', tid)
        if level is 0:
            note = None
        elif level is 1:
            note = '@here'
        elif level is 2:
            note = '@everyone'

        type = info['destinationWormholeType']['name']
        if type == "K162":
            type = info['sourceWormholeType']['name']
        system = info['destinationSolarSystem']['name']
        region = info['destinationSolarSystem']['region']['name']
        cons = info['destinationSolarSystem']['constellationID']
        cons = sdeutils.constellation(cons)
        cons = cons['name']

        embed = discord.Embed(title='Thera Alert', color=discord.Color.blurple())
        embed.set_author(name='EVE-Scout', icon_url='http://games.chruker.dk/eve_online/graphics/ids/128/20956.jpg')
        embed.set_thumbnail(url='https://www.eve-scout.com/images/eve-scout-logo.png')
        embed.add_field(name='Region', value=region, inline=False)
        embed.add_field(name='System', value=system, inline=True)
        embed.add_field(name='Constellation', value=cons, inline=True)
        embed.add_field(name='Type', value=type, inline=False)

        return await self.channel.send(content=note, embed=embed)

    async def thera(self):
        url = 'https://www.eve-scout.com/api/wormholes'
        try:
            while "TheraWatch" in self.bot.cogs:
                async with aiohttp.ClientSession() as session:
                    resp = await get(session, url)
                hole = list(resp['resp'])[0]
                hole_id = hole['id']
                print(hole_id)
                source = hole['sourceSolarSystem']
                if mc.get('last_thera') == hole_id:
                    print('matched')
                elif source['name'] == "Thera":
                    destination = hole['destinationSolarSystem']
                    if destination['id'] in self.systems:
                        await self.post(2, hole)
                    elif destination['constellationID'] in self.cons:
                        await self.post(1, hole)
                    elif destination['regionId'] in self.regions:
                        await self.post(0, hole)

                await asyncio.sleep(60)

        except Exception as e:
            print("What?")
            print(e)


def setup(killbot):
    killbot.add_cog(TheraWatch(killbot))


def teardown(killbot):
    killbot.remove_cog(TheraWatch)