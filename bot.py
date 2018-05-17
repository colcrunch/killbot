from utils.importsfile import *

if os.path.exists('utils/config.py'):
    from utils.config import logginglevel
else:
    logginglevel = 'DEBUG'

if os.path.exists('logs'):
    level = logginglevel
    logger = logging.getLogger('discord')
    logger.setLevel(level)
    handler = logging.FileHandler(filename=f'logs/discord{datetime.datetime.utcnow().strftime("%Y%m%d%H%M")}.log',
                                  encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s ::: %(levelname)s ::: %(name)s :::  %(message)s'))
    logger.addHandler(handler)
else:
    logger = None


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

    async def on_command_error(self, context, error):
        if isinstance(error, commands.NoPrivateMessage):
            await context.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await context.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.UserInputError):
            await context.send(error)
        elif isinstance(error, commands.NotOwner):
            logger.error('%s tried to run %s but is not the owner' % (context.author, context.command.name))
        elif isinstance(error, commands.CommandInvokeError):
            logger.error('In %s:' % context.command.qualified_name)
            logger.error(''.join(traceback.format_tb(error.original.__traceback__)))
            logger.error('{0.__class__.__name__}: {0}'.format(error.original))

    def run(self):
        super().run(self.token)

    async def on_ready(self):

        # Load Extensions
        for addon in self.addons:
            try:
                self.load_extension(f'extensions.{addon}')
            except Exception as e:
                logger.fatal(f'{addon} failed to load. Exception:')
                logger.fatal(e)
                print(f'{addon} FAIL')
            else:
                print(f'{addon} Loaded')

        # Load database config lists into cache.
        for guild in super().guilds:
            core.updateadmin(guild.id)
            core.load_ignore(guild.id)

        await self.change_presence(activity=discord.Game(name=self.playing))
        print('\nLogged In')
        print(self.user.name)
        print(self.user.id)
        print('------------')