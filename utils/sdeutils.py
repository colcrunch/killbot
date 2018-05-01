from utils.importsfile import *
import shutil
import bz2
import urllib
import sqlite3 as sqlite


if os.path.exists('db/sde.sqlite'):
    db = 'db/sde.sqlite'
else:
    db = None


def getfile(url):
    r = requests.get('https://www.fuzzwork.co.uk/')
    if r.status_code != 200:
        return None
    else:
        filename = url.split('/')[-1]
        urllib.request.urlretrieve(url, filename)
        return filename


def extract(file):
    with open('sde.sqlite', 'wb') as newfile, open(file, 'rb') as file:
        decompressor = bz2.BZ2Decompressor()
        for data in iter(lambda: file.read(100 * 1024), b''):
            newfile.write(decompressor.decompress(data))
    return True


def move():
    os.remove('sqlite-latest.sqlite.bz2')
    mv = shutil.move('sde.sqlite', 'db/sde.sqlite')
    return True


def exec_one(query):
    conn = sqlite.connect(db)
    c = conn.cursor()
    c.execute(query)
    t = c.fetchone()
    conn.close()

    return t


def exec_all(query):
    conn = sqlite.connect(db)
    c = conn.cursor()
    c.execute(query)
    t = c.fetchall()
    conn.close()

    return t


def type_id(name):
    query = f"SELECT typeID FROM invTypes WHERE typeName LIKE '{name}'"
    t = exec_one(query)

    if t is None:
        return None
    else:
        return str(t[0])


def type_name(tid):
    query = f'SELECT typeName FROM invTypes WHERE typeID = {tid}'
    t = exec_one(query)

    if t is None:
        return None
    else:
        return str(t[0])


def region_id(name):
    query = f"SELECT regionID FROM mapRegions WHERE regionName LIKE '{name}'"
    t = exec_one(query)

    if t is None:
        return None
    else:
        return str(t[0])


def region_name(rid):
    query = f'SELECT regionName FROM mapRegions WHERE regionID = {rid}'
    t = exec_one(query)

    if t is None:
        return None
    else:
        return str(t[0])


def constellation(cid):
    query = f'SELECT constellationName, regionID FROM mapConstellations WHERE constellationID = {cid}'
    t = exec_one(query)

    if t is None:
        return None
    else:
        return {'name': str(t[0]), 'regionID': t[1]}


def system_id(name):
    query = f"SELECT solarSystemID FROM mapSolarSystems WHERE solarSystemName LIKE '{name}'"
    t = exec_one(query)

    if t is None:
        return None
    else:
        return str(t[0])


def system_name(sid):
    query = f'SELECT solarSystemName FROM mapSolarSystems WHERE solarSystemID = {sid}'
    t = exec_one(query)

    if t is None:
        return None
    else:
        return str(t[0])


def system_star(sid):
    query = f'SELECT sunTypeID FROM mapSolarSystems WHERE solarSystemID = {sid}'
    t = exec_one(query)

    if t is None:
        return None
    else:
        return str(t[0])
