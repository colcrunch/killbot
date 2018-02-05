from utils.importsfile import *
from utils import config


class killbot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.token = config.token
        self.prefix = config.prefix
        self.playing = config.msg
        self.description = 'Killbot is a bot written in py3 for general use with EVE Online.'

        self.addons = config.addons

        super().__init__(command_prefix=self.prefix, description=self.description, pm_help=None, *args, **kwargs)

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        self.start_time = datetime.datetime.utcnow()

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