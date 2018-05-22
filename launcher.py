from bot import killbot
import sys
import utils.sdeutils as sde
import shutil
# noinspection PyPackageRequirements
import discord
import logging
import os
import utils.core as core


if os.path.exists('utils/config.py'):
    def main():
        bot = killbot()
        killbot.run(bot)
else:
    def main():
        print('No config found!\n Please run the initial setup using the setup command.\n\n'
              ' If you have already run the setup command but your config file somehow got deleted: \n'
              ' Please run the makeconfig command, then fill out config.py in the utils folder.')


def update():
    print('Downloading latest SDE... \n'
          'This might take a few mins.')
    file = sde.getfile('https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2')
    if file is None:
        print('Error Downloading SDE.')
        return print('Set Up Failed.')
    else:
        print('SDE Downloaded.')
        print('Extracting Files...')
        extract = sde.extract(file)
        if extract:
            print('Files Extracted.')
            print('Moving SDE files.')
            mv = sde.move()
            if mv:
                print('SDE Download complete.')
        else:
            print('Something went wrong when extracting the file.')
            return print('SDE Update Failed.')


def setup():
    print('Only run this set up command once! '
          'Running it after configuring your bot will likely cause issues with your config file.')
    # First get the SDE... we can use the update() function above for this.
    update()

    # Set up the bot database.
    print('Creating bot database.')
    core.botDB_create()

    #Create Log Dir.
    print("Creating Log Directory")
    try:
        os.makedirs('./logs', exist_ok=False)
    except OSError:
        pass

    print('Making configuration file.')
    shutil.copy('utils/config.py.example', 'utils/config.py')

    return print('Bot ready for configuration.')

def makeconfig():
    print('Making config file.')
    shutil.copy('utils/config.py.example', 'utils/config.py')

    return print('Please edit utils/config.py to configure your bot.')

def test():
    core.botDB_create()
    pass


def migrate():
    print('Updating bot database.')
    core.botDB_update()
    return print('Database up to date.')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif sys.argv[1] == 'setup':
        setup()
    elif sys.argv[1] == 'test':
        test()
    elif sys.argv[1] == 'update':
        update()
    elif sys.argv[1] == 'migrate':
        migrate()
    elif sys.argv[1] == 'makeconfig':
        makeconfig()
    else:
        print(sys.argv[1]+' is not a valid argument. Starting bot.')
        main()