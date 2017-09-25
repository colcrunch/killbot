import sqlite3
import config
import kb
import systemp

async def getID(system):
    conn = sqlite3.connect('systems.sqlite')
    c = conn.cursor()
    s = (system,)
    c.execute('SELECT solarSystemID FROM mapSolarSystems WHERE solarSystemName LIKE ?',s)
    t = c.fetchone()
    print(t)
    c.close()
    global systemID
    if t is None:
        systemID = "None"
    else:
        systemID = str(t[0])

async def getStats(systemID):
    if config.system_cmd.lower() == "db":
        conn = sqlite3.connect('systems.sqlite')
        c = conn.cursor
        s = (systemID,)
        c.execute('SELECT ship_kills FROM kills WHERE system = ? DESC LIMIT 24',s)
        ship_kills = c.fetchall()
        c.execute('SELECT npc_kills FROM kills WHERE system = ? DESC LIMIT 24',s)
        npc_kills = c.fetchall()
        c.execute('SELECT pod_kills FROM kills WHERE system = ? DESC LIMIT 24',s)
        pod_kills = c.fetchall()
        c.execute('SELECT jumps FROM jumps WHERE system = ? DESC LIMIT 24',s)
        jumps = c.fetchall()
        c.close()
        global stats
        if kills == None or jumps == None :
            stats = None
        else:
            kills24 = sum(ship_kills)
            npc24 = sum(npc_kills)
            pod24 = sum (pod_kills)
            jumps24 = sum(jumps)
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
        c = conn.cursor
        s = (systemID,)
        c.execute('SELECT ship_kills FROM k_tmp WHERE system = ?',s)
        ship_kills = c.fetchall()
        c.execute('SELECT npc_kills FROM k_tmp WHERE system = ?',s)
        npc_kills = c.fetchall()
        c.execute('SELECT pod_kills FROM k_tmp WHERE system = ?',s)
        pod_kills = c.fetchall()
        c.execute('SELECT jumps FROM j_tmp WHERE system = ?',s)
        jumps = c.fetchall()
        c.close()
        stats = [ship_kills,npc_kills,pod_kills,jumps]
        await systmp.clear()
