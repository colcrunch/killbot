from bot import killbot
import sys
import utils.sdeutils as sde
import shutil


def main():
    bot = killbot()
    killbot.run(bot)


def update():
    print('Downloading latest SDE... \n'
          'This might take a few mins.')
    file = sde.getfile('https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2')
    if file == None:
        print('Error Downloading SDE.')
        return print('Set Up Failed.')
    else:
        print('SDE Downloaded.')
        print('Extracting Files...')
        extract = sde.extract(file)
        if extract == True:
            print('Files Extracted.')
            print('Moving SDE files.')
            mv = sde.move()
            if mv == True:
                print('SDE Download complete.')
        else:
            print('Something went wrong when extracting the file.')
            return print('SDE Update Failed.')


def setup():
    print('Only run this set up command once! '
          'Running it after configuring your bot will likely cause issues with your config file.')
    # First get the SDE... we can use the update() function above for this.
    update()

    # Now we will copy the config file for editing.
    shutil.copy('utils/config.py.example', 'utils/config.py')
    return print('Bot ready for configuration.')


def test():
    pass

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif sys.argv[1] == 'setup':
        setup()
    elif sys.argv[1] == 'test':
        test()
    elif sys.argv[1] == 'update':
        update()
    else:
        print(sys.argv[1]+' is not a valid argument. Starting bot.')
        main()