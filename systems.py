import sqlite3
import config
import kb
import systemp
import aiohttp

async def sumFetch(tups):
    out = []
    for x in tups:
        out.append(x[0])

    return sum(out)

async def getID(system):
    conn = sqlite3.connect('sde.sqlite')
    c = conn.cursor()
    s = (system,)
    c.execute('SELECT solarSystemID FROM mapSolarSystems WHERE solarSystemName LIKE ?',s)
    t = c.fetchone()
    print(t)
    c.close()
    global systemID
    if t is None:
        systemID = None
    else:
        systemID = str(t[0])

async def getStats(systemID):
    if config.system_cmd.lower() == "db":
        conn = sqlite3.connect('systems.sqlite')
        c = conn.cursor()
        s = (systemID,)
        c.execute('SELECT ship_kills FROM kills WHERE system = ? ORDER BY id DESC LIMIT 24',s)
        ship_kills = c.fetchall()
        c.execute('SELECT npc_kills FROM kills WHERE system = ? ORDER BY id DESC LIMIT 24',s)
        npc_kills = c.fetchall()
        c.execute('SELECT pod_kills FROM kills WHERE system = ? ORDER BY id DESC LIMIT 24',s)
        pod_kills = c.fetchall()
        c.execute('SELECT jumps FROM jumps WHERE system = ? ORDER BY id DESC LIMIT 24',s)
        jumps = c.fetchall()
        conn.close()
        global stats
        if ship_kills == None or pod_kills == None or npc_kills == None or jumps == None :
            stats = None
        else:
            kills24 = await sumFetch(ship_kills)
            npc24 = await sumFetch(npc_kills)
            pod24 = await sumFetch(pod_kills)
            jumps24 = await sumFetch(jumps)
            stats = [kills24, npc24, pod24, jumps24]

    elif config.system_cmd.lower() == "esi":
        urlk = "https://esi.tech.ccp.is/latest/universe/system_kills/?datasource=tranquility"
        urlj = "https://esi.tech.ccp.is/latest/universe/system_jumps/?datasource=tranquility"
        async with aiohttp.ClientSession() as session:
            kills = await kb.fetch(session, urlk)
        async with aiohttp.ClientSession() as session:
            jumps = await kb.fetch(session, urlj)

        await systemp.getStats(kills, jumps)
        conn = sqlite3.connect('systems.sqlite')
        c = conn.cursor()
        s = (systemID,)
        c.execute('SELECT ship_kills FROM k_tmp WHERE system = ?',s)
        ship_kills = c.fetchone()
        c.execute('SELECT npc_kills FROM k_tmp WHERE system = ?',s)
        npc_kills = c.fetchone()
        c.execute('SELECT pod_kills FROM k_tmp WHERE system = ?',s)
        pod_kills = c.fetchone()
        c.execute('SELECT jumps FROM j_tmp WHERE system = ?',s)
        jumps = c.fetchone()
        conn.close()

        stats = [ship_kills[0],npc_kills[0],pod_kills[0],jumps[0]]
        await systemp.clear()
