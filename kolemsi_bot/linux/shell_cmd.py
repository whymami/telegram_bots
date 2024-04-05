import subprocess
from utils import homepage
from time import sleep

def handle_shell(bot, message):
    bot.send_message(message.chat.id, "Komut giriniz.")

    @bot.message_handler(func=lambda m: True)
    def handle_message(cmd):
        try:
            shell_command = cmd.text
            # Shell komutunu çalıştır
            result = subprocess.run(shell_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Komutun çıktısını gönder
            bot.reply_to(cmd, f"Çıktı:\n{result.stdout}")
            sleep(1)
            bot.send_message(cmd.chat.id, "İşlem tamamlandı.")
            homepage(bot, cmd, "Başka ne yapmak istersiniz?")
        except Exception as e:
            # Hata olursa hatayı gönder
            bot.reply_to(cmd, f"Hata: {e}")
            sleep(1)
            bot.send_message(cmd.chat.id, "İşlem tamamalananamadı.")
            homepage(bot, cmd, "Başka ne yapmak istersiniz?")

