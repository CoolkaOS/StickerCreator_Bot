import telegram
import logging
from telegram.ext import Updater
import cropper
from telegram.ext import CommandHandler, BaseFilter
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler
import os
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = ''

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

try:  # creats output folder if it doesn't exist
    os.mkdir('output')
except FileExistsError:
    pass
try:  # creats input folder if it doesn't exist
    os.mkdir('input')
except FileExistsError:
    pass

def start(bot, updater):
    bot.send_message(chat_id=updater.message.chat_id, text="This is Sticker Creator bot made by CoolkaOS!\nSend me your photos and I will crop them to be round!")


def hmp(bot, updater):
    bot.send_message(chat_id=updater.message.chat.id, text='Reply to this message with photos', reply_markup=telegram.ForceReply())
    time.sleep(4)
    btnlist = [
        telegram.InlineKeyboardButton('Photos.', callback_data='photos'),
        telegram.InlineKeyboardButton('Files.', callback_data='files'),
    ]
    markup = telegram.InlineKeyboardMarkup(cropper.build_menu(btnlist, n_cols=2))
    bot.send_message(chat_id=updater.message.chat.id, text='What type of output do you prefer?',
                     reply_markup=markup)

def download(bot, updater):
    if updater.message.photo:
        file_id = updater.message.photo[-1]
    else:
        file_id = updater.message.document
    newfile = bot.get_file(file_id)
    newfile.download('input/{}.png'.format(file_id['file_id'][-10:]))


def error(bot, updater):
    bot.send_message(chat_id=updater.message.chat.id, text='Error.')


def query_h(bot, updater):
    call = updater.callback_query
    if call.data == 'files':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
        cropper.crop_all()
        for file in os.listdir('output/'):
            bot.send_document(chat_id=call.message.chat.id, document=open('output/' + file, 'rb'))
        cropper.clear()
    if call.data == 'photos':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
        cropper.crop_all()
        for file in os.listdir('output/'):
            bot.send_photo(chat_id=call.message.chat.id, photo=open('output/' + file, 'rb'))
        cropper.clear()


dispatcher.add_handler(CallbackQueryHandler(query_h))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('crop', hmp))
dispatcher.add_handler(MessageHandler(Filters.reply, download))
dispatcher.add_handler(MessageHandler(Filters.chat, error))
updater.start_polling()