# coding: utf-8

import os

from telegram.ext import CommandHandler, MessageHandler, Filters

from basebot import BaseBot
from models import tuling, toutiao
from utils.utils import logger

# Set these variable to the appropriate values
TOKEN = os.environ.get('TELEGRAM_TOKEN')
NAME = os.environ.get('APP_NAME')
PORT = os.environ.get('PORT')
webhook_url = "https://{}.herokuapp.com/{}".format(NAME, TOKEN)

bb = BaseBot(TOKEN)

"""
Add handlers here
"""


@bb.handler(CommandHandler, 'toutiao')
def tt(bot, update):
    # update.effective_message.text
    tt = toutiao.Toutiao()
    r = tt.fetch('news_hot')
    reply = '*{source}*\n' \
            '[{title}]({article_url})\n' \
            '{abstract}'
    for d in r['data']:
        # logger.info(d)
        update.message.reply_markdown(
            reply.format(title=d['title'], abstract=d['abstract'], source=d['source'], article_url=d['article_url']))


# /start command
@bb.handler(CommandHandler, 'start')
def start(bot, update):
    update.message.reply_text('我是一个机器人，咱们唠嗑吧')
    # bot.sendMessage(chat_id=update.message.chat_id, text='我是一个机器人，咱们唠嗑吧')


# 图灵机器人
@bb.handler(MessageHandler, Filters.text)
def tl(bot, update):
    data = {
        'info': update.effective_message.text,
    }
    r = tuling.Tuling().text(data)
    update.effective_message.reply_text(r)


# Unset command
@bb.handler(MessageHandler, Filters.command)
def unknown(bot, update):
    update.message.reply_text('No such command:{c}'.format(c=update.effective_message.text))


# Run bot
bb.go(webhook_url=webhook_url, port=PORT)
