from utils.importsfile import *
import shutil
import bz2
import urllib

def getfile(url):
    r = requests.get('https://www.fuzzwork.co.uk/')
    if r.status_code != 200:
        return None
    else:
        filename = url.split('/')[-1]
        urllib.request.urlretrieve(url, filename)
        return filename

def extract(file):
    with open('sde.sqlite', 'wb') as newfile, open(file, 'rb') as file:
        decompressor = bz2.BZ2Decompressor()
        for data in iter(lambda : file.read(100 * 1024), b''):
            newfile.write(decompressor.decompress(data))
    return True

def rename():
    mv = shutil.move('sqlite-latest.sqlite', '../db/sde.sqlite')
    return mv
