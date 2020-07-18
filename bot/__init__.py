import logging
import os
import time

import telegram.ext as tg
from dotenv import load_dotenv

from telegraph import Telegraph

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

load_dotenv('config.env')

def getConfig(name: str):
    return os.environ[name]

LOGGER = logging.getLogger(__name__)

try:
    if bool(getConfig('_____REMOVE_THIS_LINE_____')):
        logging.error('The README.md file there to be read! Exiting now!')
        exit()
except KeyError:
    pass

BOT_TOKEN = None

AUTHORIZED_CHATS = set()

AUTHORIZED_CHATS = set()
if os.path.exists('authorized_chats.txt'):
    with open('authorized_chats.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            AUTHORIZED_CHATS.add(int(line.split()[0]))

try:
    BOT_TOKEN = getConfig('BOT_TOKEN')
    OWNER_ID = int(getConfig('OWNER_ID'))
except KeyError as e:
    LOGGER.error("One or more env variables missing! Exiting now")
    exit(1)

DRIVE_ID = []
INDEX_URL = {}

if os.path.exists('drive_index.txt'):
    count = 0
    with open('drive_index.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            temp = line.strip().split()
            DRIVE_ID.append(temp[0])
            try:
                INDEX_URL[count] = temp[1]
            except IndexError as e:
                INDEX_URL[count] = None
            count += 1

if DRIVE_ID :
    pass
else :
    LOGGER.error("Fill up drive id's in drive_index.txt")
    exit(1)


telegra_ph = Telegraph()
telegra_ph.create_account(short_name='Asta')

updater = tg.Updater(token=BOT_TOKEN,use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher
