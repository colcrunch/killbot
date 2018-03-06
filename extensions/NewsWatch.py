from utils.importsfile import *
import sqlite3 as sql


class NewsWatch:
    def __init__(self, bot):
        self.bot = bot
        print("Watching for news from CCP.")
        # self.bg_task = self.bot.loop.create_task(self.news())
        self.bot.logger.info("NewsWatch Extension loaded.")
        self.channel = config.news_channel
        self.news = config.news
        self.patch = config.patchnotes
        self.dev = config.devblogs

    @commands.command(name='news')
    async def newss(self, ctx):
        # await self.bot.wait_until_ready()
        urld = "https://www.eveonline.com/rss/json/dev-blogs"
        urln = "https://www.eveonline.com/rss/json/news"
        urlp = "https://www.eveonline.com/rss/json/patch-notes"
        try:
            async with aiohttp.ClientSession() as session:
                respd = await core.get_json(session, urld)
                respn = await core.get_json(session, urln)
                respp = await core.get_json(session, urlp)

            conn = sql.connect('db/killbot.db')
            c = conn.cursor()
            c.execute('SELECT nid FROM news')
            t = c.fetchall()
            u = []
            for s in t:
                u.append(s[0])
            conn.close()
            print(u)
            for article in respn and respd and respp:
                if article['id'] in u:
                    print(f'{article["id"]} already in database')
                else:
                    conn = sql.connect('db/killbot.db')
                    c = conn.cursor()
                    query = (f'INSERT INTO news VALUES (NULL , "{article["id"]}", "{article["title"]}", '
                            f'"{article["link"]}" , "{article["publishingDate"]}", "{article["category"]}", '
                            f'"{article["author"]}")')
                    print(query)
                    c.execute(query)
                    print(article['id'])
                    conn.commit()
                    conn.close()

        except Exception as e:
            print(e)



def setup(killbot):
    killbot.add_cog(NewsWatch(killbot))


def teardown(killbot):
    killbot.remove_cog(NewsWatch)