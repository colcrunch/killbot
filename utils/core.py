from utils.importsfile import *
import bot
import async_timeout
import sqlite3 as sql


mc = memcache.Client(['127.0.0.1:11211'], debug=1)


botDB_tables = {'news': 'CREATE TABLE news (id integer PRIMARY KEY AUTOINCREMENT UNIQUE, nid, title, url, pubDate, category, author)',
                'botAdmins': 'CREATE TABLE botAdmins (id integer PRIMARY KEY AUTOINCREMENT UNIQUE, uid, sid, idstr UNIQUE)',
                'dontListen': 'CREATE TABLE dontListen (id integer PRIMARY KEY AUTOINCREMENT UNIQUE, chid, sid, idstr UNIQUE)'}


# Cause strftime, or the time library in general does not have a real way to deal with time delta objects.
def strftdelta(tdelta):
    d = dict(days=tdelta.days)
    if d['days'] >= 365:
        d['yrs'], rem = divmod(d['days'], 365)
        d['mos'], rem = divmod(rem, 30)
        d['days'] = rem
    d['hrs'], rem = divmod(tdelta.seconds, 3600)
    d['min'], d['sec'] = divmod(rem, 60)

    if 'yrs' in d:
        fmt = '{yrs} yrs {mos} mos {days} days {hrs} hrs {min} min'
    elif d['min'] is 0:
        fmt = '{sec} sec'
    elif d['hrs'] is 0:
        fmt = '{min} min {sec} sec'
    elif d['days'] is 0:
        fmt = '{hrs} hr(s) {min} min {sec} sec'
    else:
        fmt = '{days} day(s) {hrs} hr(s) {min} min {sec} sec'

    return fmt.format(**d)


async def get_json(session, url):
    headers = {'user-agent': f'application: {config.app} contact: {config.contact}',
               'content-type': 'application/json'}
    with async_timeout.timeout(15):
        async with session.get(url, headers=headers) as response:
            json = await response.json()
            resp_code = response.status
            return {'resp': json, 'code': resp_code}


async def get_esi(session, url):
    headers = {'user-agent': f'application: {config.app} contact: {config.contact}',
               'content-type': 'application/json'}
    with async_timeout.timeout(15):
        async with session.get(url, headers=headers) as response:
            now = datetime.datetime.utcnow()
            if 'Expires' not in response.headers:
                exp_time = now - now
                bot.logger.error(f'ESI returned a response without an expiry header! HTTP Code: {response.status} | '
                                 f'Request URL: {url}')
                bot.logger.error(response.headers)
                bot.logger.error(await response.json())
            else:
                exp = datetime.datetime.strptime(response.headers['Expires'], "%a, %d %b %Y %H:%M:%S %Z")
                exp_time = exp - now
            json = await response.json()
            resp_code = response.status
            return {'resp': json, 'exp': exp_time, "code": resp_code}


def botDB_create():
    conn = sql.connect('db/killbot.db')
    c = conn.cursor()
    for table in botDB_tables:
        c.execute(botDB_tables[table])
    conn.commit()
    conn.close()
    return


def botDB_update():
    conn = sql.connect('db/killbot.db')
    c = conn.cursor()
    c.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    t = c.fetchall()
    current = []
    for u in t:
        current.append(u[0])
    for table in botDB_tables:
        if table not in current:
            print(f'Creating {table} table in bot database.')
            c.execute(botDB_tables[table])
    conn.commit()
    conn.close()
    return


def promote(uid, sid):
    conn = sql.connect('db/killbot.db')
    c = conn.cursor()
    query = f'INSERT INTO botAdmins VALUES (NULL, {uid}, {sid}, "{uid}{sid}")'
    c.execute(query)
    conn.commit()
    conn.close()
    return


def demote(uid, sid):
    admins = mc.get(f'{sid}_admin')
    if uid not in admins:
        # sqlite3 doesn't raise an error when you try to delete a record that doesn't exist, so we will check first,
        # then raise it if we need to. (using this error for convenience)
        raise sql.IntegrityError
    conn = sql.connect('db/killbot.db')
    c = conn.cursor()
    query = f'DELETE FROM botAdmins WHERE idstr = "{uid}{sid}"'
    c.execute(query)
    conn.commit()
    conn.close()
    return


def updateadmin(sid):
    if mc.get(f'{sid}_admin') is not None:
        mc.delete(f'{sid}_admin')
    conn = sql.connect('db/killbot.db')
    c = conn.cursor()
    query = f'SELECT * FROM botAdmins WHERE sid = {sid}'
    c.execute(query)
    t = c.fetchall()
    conn.close()
    admins = []
    for ent in t:
        admins.append(ent[1])
    mc.set(f'{sid}_admin', admins)
    return


def link_ignore(chid, sid):
    conn = sql.connect('db/killbot.db')
    c = conn.cursor()
    query = f'INSERT INTO dontListen VALUES (NULL, {chid}, {sid}, "{chid}#{sid}")'
    c.execute(query)
    conn.commit()
    conn.close()
    return


def load_ignore(sid):
    if mc.get(f'{sid}_dontListen') is not None:
        mc.delete(f'{sid}_dontListen')
    conn = sql.connect('db/killbot.db')
    c = conn.cursor()
    query = f'SELECT chid FROM dontListen WHERE sid = {sid}'
    c.execute(query)
    t =  c.fetchall()
    ignores = []
    for u in t:
        ignores.append(u[0])
    mc.set(f'{sid}_dontListen', ignores)
    return


def stop_ignore(chid, sid):
    ignores = mc.get(f'{sid}_dontListen')
    if chid not in ignores:
        raise sql.IntegrityError
    conn = sql.connect('db/killbot.db')
    c = conn.cursor()
    query = f'DELETE FROM dontListen WHERE idstr = {chid}#{sid}'
    c.execute(query)
    conn.commit()
    conn.close()
    return

