from utils.importsfile import *
from utils import config
from utils.config import logginglevel

level = logginglevel
logger = logging.getLogger('discord')
logger.setLevel(level)
handler = logging.FileHandler(filename=f'logs/discord{datetime.datetime.utcnow().strftime("%Y%m%d%H%M")}.log',
                              encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s ::: %(levelname)s ::: %(name)s :::  %(message)s'))
logger.addHandler(handler)

class killbot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.token = config.token
        self.prefix = config.prefix
        self.playing = config.msg
        self.description = 'Killbot is a bot written in py3 for general use with EVE Online.'
        self.start_time = datetime.datetime.utcnow()

        self.addons = config.addons
        self.counter = 0
        self.lcounter = 0
        self.kcounter = 0
        self.logger = logger

        super().__init__(command_prefix=self.prefix, description=self.description, pm_help=None, *args, **kwargs)

    def run(self):
        super().run(self.token)

    async def on_ready(self):

        for addon in self.addons:
            try:
                self.load_extension(f'extensions.{addon}')
            except Exception as e:
                # TODO: Log exception when we actually do logging.
                print(f'{addon} FAIL')
            else:
                print(f'{addon} Loaded')

        await self.change_presence(game=discord.Game(name=self.playing))
        print('\nLogged In')
        print(self.user.name)
        print(self.user.id)
        print('------------')