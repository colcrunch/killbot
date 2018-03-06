from utils.importsfile import *
import async_timeout
import sqlite3 as sql

mc = memcache.Client(['127.0.0.1:11211'], debug=1)

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
    headers = {'user-agent': 'application: {0} contact: {1}'.format(config.app, config.contact),
               'content-type': 'application/json'}
    with async_timeout.timeout(15):
        async with session.get(url, headers=headers) as response:
            return await response.json()

async def get_esi(session, url):
    headers = {'user-agent': 'application: {0} contact: {1}'.format(config.app, config.contact),
               'content-type': 'application/json'}
    with async_timeout.timeout(15):
        async with session.get(url, headers=headers) as response:
            now  = datetime.datetime.utcnow()
            exp = datetime.datetime.strptime(response.headers['Expires'], "%a, %d %b %Y %H:%M:%S %Z")
            exp_time = exp - now
            json = await response.json()
            return {'resp': json, 'exp': exp_time}

def botDB_create():
    conn = sql.connect('db/killbot.db')
    c = conn.cursor()
    c.execute('CREATE TABLE news (id integer PRIMARY KEY AUTOINCREMENT UNIQUE, nid, title, url, pubDate, category, author)')
    conn.close()
    return