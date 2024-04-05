import os
from time import sleep
from turtle import home
from requests import delete
from telebot import types

from utils import delete_message, homepage, delete_message_with_buttons

# Dizin geçmişi için bir liste oluşturun
directory_history = []

def handle_buttons(bot, call):
    # Geri butonuna basıldıysa bir önceki dizine git
    if call.data == 'back':
        # Dizin geçmişindeki bir önceki dizini al, eğer bir önceki dizin yoksa hata mesajı gönder
        try:
            directory_history.pop()
            send_directory_listing(bot, call.message)
        except IndexError:
            bot.send_message(call.message.chat.id, "Root dizinindesiniz.")
    elif call.data == 'HomePage':
        homepage(bot, call.message, "Başlamak için bir işlem seçin.")
        sleep(0.2)
        delete_message_with_buttons(bot, call.message.chat.id, call.message.message_id)
    # Dizin butonuna basıldıysa o dizine gir
    elif os.path.isdir(call.data):
        directory_history.append(call.data)
        send_directory_listing(bot, call.message)
    # Dosya butonuna basıldıysa dosya içeriğini gönder
    else:
        send_file_content(bot, call.message, call.data)

def send_directory_listing(bot, message):
    # Mevcut dizini al
    current_directory = directory_history[-1]

    # Dizin içeriğini al (gizli dosyaları gösterme)
    try:
        directory_contents = [entry.name for entry in os.scandir(current_directory) if not entry.name.startswith('.')]
    except Exception as e:
        bot.send_message(message.chat.id, f"Hata: {e}")
        return  # Fonksiyondan çık

    # Butonları oluştur
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Dosya ve dizinleri listeleyerek butonları ekle
    for item in directory_contents:
        item_path = os.path.join(current_directory, item)
        if os.path.isdir(item_path):
            markup.add(types.InlineKeyboardButton(item, callback_data=item_path))
        else:
            markup.add(types.InlineKeyboardButton(item, callback_data=item_path))

    # Geri butonunu ekle (ana dizinde değilse)
    if current_directory != "/home":
        markup.add(types.InlineKeyboardButton("Back", callback_data="back"))
        markup.add(types.InlineKeyboardButton("/Home", callback_data="/home"))
        markup.add(types.InlineKeyboardButton("Home Page", callback_data="HomePage"))
    if current_directory == "/home":
        markup.add(types.InlineKeyboardButton("Home Page", callback_data="HomePage"))

    # Mesajı gönder
    bot.send_message(message.chat.id, f"Current Directory: {current_directory}", reply_markup=markup)

def send_file_content(bot, message, file_path):
    # Dosya içeriğini gönder
    try:
        with open(file_path, "rb") as file:
            bot.send_document(message.chat.id, file)
        delete_message(bot, message.chat.id, message.message_id)
        homepage(bot, message, "Başlamak için bir işlem seçin.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Hata: {e}")