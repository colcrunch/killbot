from utils.importsfile import *
import shutil
import bz2
import urllib
import sqlite3 as sqlite


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
        for data in iter(lambda : file.read(100 * 1024), b''):
            newfile.write(decompressor.decompress(data))
    return True


def move():
    os.remove('sqlite-latest.sqlite.bz2')
    mv = shutil.move('sde.sqlite', 'db/sde.sqlite')
    return True


def type_id(name):
    db = 'db/sde.sqlite'
    conn = sqlite.connect(db)
    c = conn.cursor()
    n = (name,)
    c.execute('SELECT typeID FROM invTypes WHERE typeName LIKE ?', n)
    t = c.fetchone()
    conn.close()

    if t is None:
        return None
    else:
        return str(t[0])


def type_name(tid):
    db = 'db/sde.sqlite'
    conn = sqlite.connect(db)
    c = conn.cursor()
    n = (tid,)
    c.execute('SELECT typeName FROM invTypes WHERE typeID = ?', n)
    t = c.fetchone()
    conn.close()

    if t is None:
        return None
    else:
        return str(t[0])


def region_id(name):
    db = 'db/sde.sqlite'
    conn = sqlite.connect(db)
    c = conn.cursor()
    n = (name,)
    c.execute('SELECT regionID FROM mapRegions WHERE regionName LIKE ?', n)
    t = c.fetchone()
    conn.close()

    if t is None:
        return None
    else:
        return str(t[0])

def region_name(rid):
    db = 'db/sde.sqlite'
    conn = sqlite.connect(db)
    c = conn.cursor()
    n = (rid,)
    c.execute('SELECT regionName FROM mapRegions WHERE regionID = ?', n)
    t = c.fetchone()
    conn.close()

    if t is None:
        return None
    else:
        return str(t[0])

def constellation(cid):
    db = 'db/sde.sqlite'
    conn = sqlite.connect(db)
    c = conn.cursor()
    n = (cid,)
    c.execute('SELECT constellationName, regionID FROM mapConstellations WHERE constellationID = ?', n)
    t = c.fetchone()
    conn.close()

    if t is None:
        return None
    else:
        return {'name': str(t[0]), 'regionID': t[1]}

def system_id(name):
    db = 'db/sde.sqlite'
    conn = sqlite.connect(db)
    c = conn.cursor()
    n = (name,)
    c.execute('SELECT solarSystemID FROM mapSolarSystems WHERE solarSystemName LIKE ?', n)
    t = c.fetchone()
    conn.close()

    if t is None:
        return None
    else:
        return str(t[0])


def system_name(sid):
    db = 'db/sde.sqlite'
    conn = sqlite.connect(db)
    c = conn.cursor()
    n = (sid,)
    c.execute('SELECT solarSystemName FROM mapSolarSystems WHERE solarSystemID = ?', n)
    t = c.fetchone()
    conn.close()

    if t is None:
        return None
    else:
        return str(t[0])

def system_star(sid):
    db = 'db/sde.sqlite'
    conn = sqlite.connect(db)
    c = conn.cursor()
    n = (sid,)
    c.execute('SELECT sunTypeID FROM mapSolarSystems WHERE solarSystemID = ?', n)
    t = c.fetchone()
    conn.close()

    if t is None:
        return None
    else:
        return str(t[0])