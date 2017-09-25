import sqlite3
import config
import kb

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

async def getStats(systemID)
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
            npc = sum(npc_kills)
            pod = sum (pod_kills)
            jumps24 = sum(jumps)
            stats = [kills24, npc, pod, jumps24]
    elif config.system_cmd.lower() == "esi":
        urlk = "https://esi.tech.ccp.is/latest/universe/system_kills/?datasource=tranquility"
        urlj = "https://esi.tech.ccp.is/latest/universe/system_jumps/?datasource=tranquility"
        async with aiohttp.ClientSession() as session:
            kills = await kb.fetch(session, urlk)
        async with aiohttp.ClientSession() as session:
            jumps = await kb.fetch(session, urlj)
