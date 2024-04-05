import zipfile
import telebot
import os
from time import sleep

#my library
from utils import homepage

def wait_for_zip(bot, message):
    bot.send_message(message.chat.id, "Almak istediğin klasörün yolunu yazın. (örn: /home/user/Desktop/folder)")

    @bot.message_handler(func=lambda m: True)
    def handle_zip(message):
        try:
            # Klasör yolunu al
            folder_path = message.text
            
            # ZIP dosyasının adını belirle
            zip_file_name = os.path.basename(folder_path) + ".zip"
            zip_file_path = os.path.join("resimler", zip_file_name)

            # ZIP dosyasını oluştur
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                # Klasör içeriğini dolaşarak her dosyayı ZIP dosyasına ekle
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, arcname=os.path.relpath(file_path, folder_path))

            # ZIP dosyasını gönder
            with open(zip_file_path, 'rb') as zip_file:
                bot.send_document(message.chat.id, zip_file)
            sleep(1)
            bot.send_message(message.chat.id, "ZIP dosyası gönderildi.")
            homepage(bot, message, "Başka ne yapmak istersiniz?")
            # ZIP dosyasını sil
            os.remove(zip_file_path)

            return True, "Klasör başarıyla ZIP dosyası olarak gönderildi."
        except Exception as e:
            error_message = f"Hata: {e}"
            return False, error_message