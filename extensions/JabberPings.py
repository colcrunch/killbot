from utils.importsfile import *
import aioxmpp
import re


class JabberPings:
    def __init__(self, bot):
        self.bot = bot
        self.jid = aioxmpp.JID.fromstr(config.user_jid)
        self.password = config.user_password
        self.channel = self.bot.get_channel(config.ping_channel)
        self.icon_url = config.logo_url

        self.target = config.broadcast_jid
        self.bg_task = self.bot.loop.create_task(self.jabber(self.jid, self.password))

    async def jabber(self, jid, password):
        await self.bot.wait_until_ready()
        print('Waiting for pings from Jabber.')
        client = aioxmpp.PresenceManagedClient(jid, aioxmpp.make_security_layer(password, no_verify=True))

        icon_url = self.icon_url
        bot = self.bot

        def message_recieved(msg):
            if not msg.body:
                # We dont want to do anything with an empty message.
                return

            if msg.from_.bare() == aioxmpp.JID.fromstr(self.target).bare():
                # Take the message and pass it to an async task so we can post it.
                return asyncio.Task(post(msg))
            return

        message_dispatcher = client.summon(aioxmpp.dispatcher.SimpleMessageDispatcher)
        message_dispatcher.register_callback(aioxmpp.MessageType.CHAT, None, message_recieved)

        async def post(msg):
            body = msg.body[list(msg.body.keys())[0]]
            bot.logger.info('Ping Received.')
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
            if len(urls) == 0:
                urlstr = ''
            else:
                urlstr = "**PING CONTAINS THE FOLLOWING URLS** \n> " + ' \n> '.join(urls) + "\n\n"
            time = datetime.datetime.utcnow()
            embed = discord.Embed(description=f'```\n{body}```\n '
                                              f'{urlstr}'
                                              f'***THIS IS PING HAS BEEN AUTOMATICALLY FORWARDED FROM JABBER***',
                                  color=discord.Color.red(), timestamp=time)
            embed.set_author(name=f'{self.target}', icon_url=f'{icon_url}')
            embed.set_thumbnail(url=f'{icon_url}')
            embed.set_footer(icon_url=bot.user.avatar_url_as(format='png'), text=f"Service provided by {bot.user.name}")
            return await self.channel.send(embed=embed)

        @aioxmpp.service.iq_handler()
        async def iq_handle():
            pass

        async with client.connected():
            while 'JabberPings' in self.bot.cogs:
                await asyncio.sleep(1)


def setup(killbot):
    killbot.add_cog(JabberPings(killbot))


def teardown(killbot):
    killbot.remove_cog(JabberPings)