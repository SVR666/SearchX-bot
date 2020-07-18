from telegram.message import Message
from telegram.update import Update
import time
from bot import LOGGER, bot
from telegram.error import TimedOut, BadRequest
from bot import bot
from telegram import InlineKeyboardMarkup


def sendMessage(text: str, bot, update: Update):
    try:
        return bot.send_message(update.message.chat_id,
                            reply_to_message_id=update.message.message_id,
                            text=text, parse_mode='HTMl')
    except Exception as e:
        LOGGER.error(str(e))

def editMessage(text: str, message: Message, reply_markup=None):
    try:
        bot.edit_message_text(text=text, message_id=message.message_id,
                              chat_id=message.chat.id,reply_markup=reply_markup,
                              parse_mode='HTMl')
    except Exception as e:
        LOGGER.error(str(e))

def sendLogFile(bot, update: Update):
    with open('log.txt', 'rb') as f:
        bot.send_document(document=f, filename=f.name,
                          reply_to_message_id=update.message.message_id,
                          chat_id=update.message.chat_id)
