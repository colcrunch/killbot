from utils.importsfile import *
import async_timeout

# Cause strftime, or the time library in general does not have a real way to deal with time delta objects.
def strftdelta(tdelta):
    d = dict(days=tdelta.days)
    print(str(tdelta))
    d['hrs'], rem = divmod(tdelta.seconds, 3600)
    d['min'], d['sec'] = divmod(rem, 60)

    if d['min'] is 0:
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