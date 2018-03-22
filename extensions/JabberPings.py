from utils.importsfile import *
import aioxmpp

class JabberPings:
    def __init__(self, bot):
        self.bot = bot
        self.jid = config.user_jid
        self.password = config.user_password
        self.channel = self.bot.get_channel(config.ping_channel)

        self.bg_task = self.bot.loop.create_task(self.jabber(self.jid, self.password))

    async def jabber(self, jid, password):
        client = aioxmpp.PresenceManagedClient(jid, aioxmpp.make_security_layer(password))

        def message_recieved(msg):
            if not msg.body:
                return

            print(msg.body)

        message_dispatcher = client.summon(aioxmpp.dispatcher.SimpleMessageDispatcher)
        message_dispatcher.register_callback(aioxmpp.MessageType.CHAT, None, message_recieved)

        async with client.connected():
            while 'JabberPings' in self.bot.cogs:
                await asyncio.sleep(1)


def setup(killbot):
    killbot.add_cog(JabberPings(killbot))

def teardown(killbot):
    killbot.remove_cog(JabberPings)