import sqlite3
import json
import asyncio

async def getStats(kills, jumps):
    conn = sqlite3.connect('systems.sqlite')
    c = conn.cursor()

    ktotal = []
    for x in kills:
        sys = x["system_id"]
        skills = x["ship_kills"]
        nkills = x["npc_kills"]
        pkills = x["pod_kills"]

        ktotal.append((sys, skills, nkills, pkills))


    c.executemany('INSERT INTO k_tmp VALUES (?,?,?,?)',ktotal)
    conn.commit()

    jtotal = []
    for x in jumps:
        sys = x["system_id"]
        sjumps = x["ship_jumps"]

        jtotal.append((sys, sjumps))

    c.executemany('INSERT INTO j_tmp VALUES (?,?)',jtotal)
    conn.commit()
    conn.close()

async def clear():
    conn = sqlite3.connect('systems.sqlite')
    c = conn.cursor
    c.execute('DELETE FROM k_tmp; DELETE FROM j_tmp')
    conn.commit()
    conn.close()
