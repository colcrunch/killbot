import sqlite3
import json
import asyncio
import re

def regexp(pattern, input):
    return bool(re.match(pattern, input))

async def getStats(kills, jumps):
    regg = '[Jj]([0-9]{6})'
    conn = sqlite3.connect('sde.sqlite')
    conn.create_function("regexp", 2, regexp)
    c = conn.cursor()
    c.execute("SELECT solarSystemID from mapSolarSystems WHERE solarSystemName NOT regexp :pattern", {'pattern': regg})
    sysids = c.fetchall()
    print(len(sysids))
    conn.close()
    
    conn = sqlite3.connect('systems.sqlite')
    c = conn.cursor()

    ktotal = []
    kids = []
    for x in kills:
        sys = x["system_id"]
        skills = x["ship_kills"]
        nkills = x["npc_kills"]
        pkills = x["pod_kills"]

        ktotal.append((sys, skills, nkills, pkills))
        kids.append(sys)

    for sysid in sysids:
        if sysid[0] not in kids:
            ktotal.append((sysid[0], 0, 0, 0))
        else:
            pass


    c.executemany('INSERT INTO k_tmp VALUES (?,?,?,?)',ktotal)
    conn.commit()

    jtotal = []
    jids = []
    for x in jumps:
        sys = x["system_id"]
        sjumps = x["ship_jumps"]

        jtotal.append((sys, sjumps))
        jids.append(sys)

    for sysid in sysids:
        if sysid[0] not in jids:
            jtotal.append((sysid[0], 0))
        else:
            pass

    c.executemany('INSERT INTO j_tmp VALUES (?,?)',jtotal)
    conn.commit()
    conn.close()

async def clear():
    conn = sqlite3.connect('systems.sqlite')
    c = conn.cursor()
    c.execute('DELETE FROM k_tmp;')
    c.execute('DELETE FROM j_tmp;')
    c.execute('VACUUM')
    conn.commit()
    conn.close()
