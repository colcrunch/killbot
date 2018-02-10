from utils.importsfile import *

class WatchRedisq:
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0
        self.lcounter = 0
        self.kcounter = 0
        self.ids = config.kill_ids
        print(f'--------------------------------------\n'
              f'Watching:\n'
              f'Characters: {", ".join(self.ids["character_id"])}\n'
              f'Corps: {", ".join(self.ids["corporation_id"])}\n'
              f'Alliances: {", ".join(self.ids["alliance_id"])}\n'
              f'Ship Types: {", ".join(self.ids["ship_type_id"])}\n'
              f'--------------------------------------')

        self.bg_task = self.bot.loop.create_task(self.watch())

    async def watch(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(config.kill_channel)
        ids = self.ids
        keys = {'alliance_id', 'corporation_id', 'character_id', 'ship_type_id'}

        url = "http://redisq.zkillboard.com/listen.php"
        try:
            while 'WatchRedisq' in self.bot.cogs:
                async with aiohttp.ClientSession() as session:
                    resp = await core.get_json(session, url)
                if resp['package'] is not None:
                    km = resp['package']['killmail']
                    attackers = km['attackers']
                    for attacker in attackers:
                        for key in keys:
                            if key in attacker:
                                if str(attacker[key]) in ids[key]:
                                    print(f"{key} YES")
                                else:
                                    print(f"{key} No")
                            else:
                                print(f"{key} Not present")

                await asyncio.sleep(10)



        except Exception as e:
            print(e)
            pass


def setup(killbot):
    killbot.add_cog(WatchRedisq(killbot))


def teardown(killbot):
    killbot.remove_cog(WatchRedisq)