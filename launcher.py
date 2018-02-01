from bot import killbot
import sys
import utils.sdeutils as sde
import os

def main():
    bot = killbot()
    killbot.run(bot)

def setup():
    print('Only use this command on first install.')
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
            print('Ensuring SDE file name is correct.')

        else:
            print('Something went wrong when extracting the file.')
            return print('Set Up Failed.')

def test():
    print(os.getcwd())
    return

if __name__ == '__main__':
    if sys.argv[1] == None:
        main()
    elif sys.argv[1] == 'setup':
        setup()
    elif sys.argv[1] == 'test':
        test()
    else:
        print(sys.argv[1]+' is not a valid argument. Starting bot.')
        main()