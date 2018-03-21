from utils.importsfile import *
import re


class SysCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sys'])
    async def system(self, ctx, *, system: str):
        """ Returns information about a system. """
        sysid = sdeutils.system_id(system)
        if sysid is None:
            return await ctx.send('System not found.')

        sys = sdeutils.system_name(sysid)
        if re.match(r'[Jj]([0-9]{6})', sys) or sys == "Thera":
            return await ctx.send('System Information not available for wormhole systems.')
        jump_dict = await esiutils.esi_sysJumps()
        kill_dict = await esiutils.esi_sysKills()

        for sys in jump_dict:
            if str(sys['system_id']) == sysid:
                jumps = sys['ship_jumps']
                break
        else:
            jumps = 0
        for sys in kill_dict:
            if str(sys['system_id']) == sysid:
                ship_kills = sys['ship_kills']
                npc_kills = sys['npc_kills']
                pod_kills = sys['pod_kills']
                break
        else:
            ship_kills = 0
            npc_kills = 0
            pod_kills = 0

        sysinfo = await esiutils.esi_system(sysid)
        const = sdeutils.constellation(sysinfo['const'])
        region = sdeutils.region_name(const['regionID'])
        sun = sdeutils.system_star(sysid)

        dotlan = f'http://evemaps.dotlan.net/system/{sysid}/'
        zkill = f'https://zkillboard.com/system/{sysid}/'

        embed = discord.Embed(title=f'{sysinfo["name"]} System Information')
        embed.set_author(name='CCP Games',
                         icon_url='https://upload.wikimedia.org/wikipedia/en/thumb/5/51/CCP_Games_Logo.svg/'
                                  '1280px-CCP_Games_Logo.svg.png')
        embed.set_thumbnail(url=f'https://imageserver.eveonline.com/Type/{sun}_64.png')
        embed.add_field(name='Sec Status / Class', value=f'{str(sysinfo["sec"])} / {sysinfo["secClass"]}')
        embed.add_field(name='Region (Constellation)', value=f'{region} ({const["name"]})')
        embed.add_field(name='Planets / Moons', value=f'{sysinfo["planets"]} / {sysinfo["moons"]}')
        if sysinfo['gates'] is not None:
            embed.add_field(name='Stargates', value=sysinfo['gates'])
        embed.add_field(name='Stats (Last Hour)', value=f'**Jumps:** {jumps} \n**Ship Kills**: {ship_kills} \n'
                                                        f'**NPC Kills:** {npc_kills}\n'
                                                        f'**Pod Kills:** {pod_kills}',
                        inline=False)
        embed.add_field(name='Additional Info', value=f'{dotlan} \n{zkill}')

        return await ctx.send(embed=embed)



def setup(killbot):
    killbot.add_cog(SysCommands(killbot))


def teardown(killbot):
    killbot.remove_cog(SysCommands)