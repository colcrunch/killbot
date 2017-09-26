import requests
import json
import sqlite3

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

regg = r'[Jj]([0-9]{6})'
conn = sqlite3.connect('sde.sqlite')
conn.create_function("REGEXP", 2, regexp)
c = conn.cursor()
c.execute("SELECT solarSystemID from mapSolarSystems WHERE solarSystemName NOT REGEXP ?", regg)
sysids = c.fetchall()
conn.close()

urlk = "https://esi.tech.ccp.is/latest/universe/system_kills/?datasource=tranquility"
headers = {'user-agent': 'application: https://github.com/colcrunch/killbot contact: rhartnett35@gmail.com','content-type': 'application/json'}
r = requests.get(urlk, headers=headers)
kills = r.json()
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

c.executemany('INSERT INTO kills VALUES (?,?,?,?)',ktotal)
conn.commit()


urlk = "https://esi.tech.ccp.is/latest/universe/system_jumps/?datasource=tranquility"
headers = {'user-agent': 'application: https://github.com/colcrunch/killbot contact: rhartnett35@gmail.com','content-type': 'application/json'}
r = requests.get(urlk, headers=headers)
jumps = r.json()


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

c.executemany('INSERT INTO jumps VALUES (?,?)',jtotal)
conn.commit()
conn.close()
print("Database updated")
