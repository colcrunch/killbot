from utils.importsfile import *
import sqlite3 as sql

# TODO: Logging


class NewsWatch:
    def __init__(self, bot):
        self.bot = bot
        print("Watching for news from CCP.")
        self.bg_task = self.bot.loop.create_task(self.newss())
        self.bot.logger.info("NewsWatch Extension loaded.")
        self.channel = config.news_channel
        self.news = config.news
        self.patch = config.patchnotes
        self.dev = config.devblogs

    async def newss(self):
        await self.bot.wait_until_ready()
        urld = "https://www.eveonline.com/rss/json/dev-blogs"
        urln = "https://www.eveonline.com/rss/json/news"
        urlp = "https://www.eveonline.com/rss/json/patch-notes"
        try:
            while 'NewsWatch' in self.bot.cogs:
                async with aiohttp.ClientSession() as session:
                    respd = await core.get_json(session, urld)
                    respn = await core.get_json(session, urln)
                    respp = await core.get_json(session, urlp)

                resp = [respd, respn, respp]
                conn = sql.connect('db/killbot.db')
                c = conn.cursor()
                c.execute('SELECT nid FROM news')
                t = c.fetchall()
                u = []
                for s in t:
                    u.append(s[0])
                for respo in resp:
                    for article in respo:
                        if article['id'] in u:
                            # Already posted
                            print(f'{article["id"]} already in database')
                        else:
                            # If we enter this section, then we want to post the article.
                            query = (f'INSERT INTO news VALUES (NULL , "{article["id"]}", "{article["title"]}", '
                                    f'"{article["link"]}" , "{article["publishingDate"]}", "{article["category"]}", '
                                    f'"{article["author"]}")')
                            # print(query)
                            c.execute(query)
                            # print(article['id'])
                            conn.commit()

                            # Build Embed
                            if article['publishingDate'].endswith("Z"):
                                time = datetime.datetime.strptime(article['publishingDate'], '%Y-%m-%dT%H:%M:%SZ')
                            else:
                                time = datetime.datetime.strptime(article['publishingDate'], '%Y-%m-%dT%H:%M:%S')
                            embed = discord.Embed(title=f'{article["title"]} ({article["category"]})', timestamp=time)
                            embed.set_author(name=f'{article["author"]}', icon_url='https://upload.wikimedia.org/wikipedia/en/'
                                                                                   'thumb/5/51/CCP_Games_Logo.svg/'
                                                                                   '1280px-CCP_Games_Logo.svg.png')
                            embed.add_field(name="Link", value=f'{article["link"]}')

                            print(f'{embed} {article["category"]}')
                            await self.channel.send(embed=embed)
                conn.close()

                await asyncio.sleep(300)

            except Exception as e:
                print(e)
                self.bg_task = self.bot.loop.create_task(self.newss())




def setup(killbot):
    killbot.add_cog(NewsWatch(killbot))


def teardown(killbot):
    killbot.remove_cog(NewsWatch)