import requests
import json
import sqlite3


urlk = "https://esi.tech.ccp.is/latest/universe/system_kills/?datasource=tranquility"
headers = {'user-agent': 'application: https://github.com/colcrunch/killbot contact: rhartnett35@gmail.com','content-type': 'application/json'}
r = requests.get(urlk, headers=headers)
kills = r.json()
conn = sqlite3.connect('systems.sqlite')
c = conn.cursor()

ktotal = []
for x in kills:
    sys = x["system_id"]
    skills = x["ship_kills"]
    nkills = x["npc_kills"]
    pkills = x["pod_kills"]

    ktotal.append((sys, skills, nkills, pkills))
    print(sys)


c.executemany('INSERT INTO kills VALUES (?,?,?,?)',ktotal)
conn.commit()


urlk = "https://esi.tech.ccp.is/latest/universe/system_jumps/?datasource=tranquility"
headers = {'user-agent': 'application: https://github.com/colcrunch/killbot contact: rhartnett35@gmail.com','content-type': 'application/json'}
r = requests.get(urlk, headers=headers)
jumps = r.json()


jtotal = []
for x in jumps:
    sys = x["system_id"]
    sjumps = x["ship_jumps"]

    jtotal.append((sys, sjumps))
    print(sys)


c.executemany('INSERT INTO jumps VALUES (?,?)',jtotal)
conn.commit()
conn.close()
print("Database updated")