import pyautogui
from PIL import Image
import telebot
from telebot import types
import os
from time import sleep
import time
from threading import Timer

#my library
from utils import homepage

def wait_for_photo(bot, message):
    bot.send_message(message.chat.id, "Lütfen göndermek istediğiniz resmi yükleyin.")

    @bot.message_handler(content_types=['photo'])
    def handle_photo(img):
        try:
            file_id = img.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = os.path.join("resimler", f"{file_id}.jpg")
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            img = Image.open(file_path)
            img.show()
            os.remove(file_path)
            sleep(1)
            bot.send_message(message.chat.id, "Resim gönderildi.")
            homepage(bot, img, "Başka ne yapmak istersiniz?")
        except Exception as e:
            bot.send_message(message.chat.id, f"Hata: {e}")


# Ardışık mesaj göndermeyi engellemek için bir bekleme süresi belirleyin (saniye cinsinden)
WAIT_TIME_SECONDS = 60

# Son mesaj gönderme zamanını saklamak için bir sözlük kullanın
last_message_times = {}

def wait_for_text(bot, message):
    chat_id = message.chat.id
    
    # Son mesaj gönderme zamanını kontrol et
    last_message_time = last_message_times.get(chat_id, 0)
    current_time = time.time()

    # Belirli bir süre geçmeden önce yeni bir mesaj gönderilmesini engelle
    if current_time - last_message_time < WAIT_TIME_SECONDS:
        remaining_time = int(WAIT_TIME_SECONDS - (current_time - last_message_time))
        bot.send_message(chat_id, f"Yeni bir mesaj göndermek için lütfen {remaining_time} saniye bekleyin.")
        homepage(bot, message, "Başka ne yapmak istersiniz?")
        return
    
    bot.send_message(chat_id, "Lütfen göndermek istediğiniz mesajı yazın.")

    @bot.message_handler(func=lambda m: True)
    def handle_text(msg1):
        chat_id = msg1.chat.id
        msg = msg1.text
        
        # Son mesaj gönderme zamanını güncelle
        last_message_times[chat_id] = time.time()

        if len(msg) <= 1000:
            # Mesajın uzunluğu 1000 karakterden azsa, tamamını gönder
            bot.send_message(chat_id, "Mesaj gönderildi:\n")
            bot.send_message(chat_id, f"Yeni bir mesaj göndermek için lütfen {WAIT_TIME_SECONDS} saniye bekleyin.")
            homepage(bot, msg1, "Başka ne yapmak istersiniz?")
            pyautogui.alert(msg)
        else:
            # Mesajın uzunluğu 1000 karakterden fazlaysa, sadece ilk 1000 karakteri gönder
            bot.send_message(chat_id, "Mesajın tamamı gönderilemedi. İlk 1000 karakter:\n" + msg[:1000])

        # Ardışık mesaj göndermeyi engellemek için bir uyarı mesajı gönder

        # Ardışık mesaj göndermeyi engellemek için bir bekleme süresi belirleyin
        Timer(WAIT_TIME_SECONDS, reset_last_message_time, args=[chat_id]).start()


def reset_last_message_time(chat_id):
    # Son mesaj gönderme zamanını sıfırla
    last_message_times[chat_id] = 0

