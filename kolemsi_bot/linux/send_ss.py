import pyautogui
from io import BytesIO
import telebot
from telebot import types
from time import sleep

#my library
from utils import homepage


def send_screen(bot, message):
    # Ekran görüntüsü al
    screenshot = pyautogui.screenshot()
    # Görüntüyü bir byte dizisine dönüştür
    img_byte_array = BytesIO()
    screenshot.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)
    bot.send_message(message.chat.id, "Ekran görüntüsü gönderildi.")
    # Görüntüyü gönder
    bot.send_photo(message.chat.id, img_byte_array)
    sleep(1)
    homepage(bot, message, "Başka ne yapmak istersiniz?")