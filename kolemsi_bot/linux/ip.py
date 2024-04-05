import subprocess
from time import sleep
from utils import homepage

def get_ip(bot, call):
    try:
        # Komutu çalıştır ve çıktıyı al
        output = subprocess.check_output(["ifconfig", "eth0"]).decode("utf-8")
        # Çıktıyı satır satır ayır
        lines = output.split("\n")
        # İlgili satırı al
        ip_line = next(line for line in lines if "inet " in line)
        # İlgili satırı parçala
        ip_parts = ip_line.split()
        # IP adresini, netmask'ı ve broadcast adresini al
        ip_address = ip_parts[1]
        netmask = ip_parts[3]
        broadcast = ip_parts[5]
        # Mac adresini al
        mac_line = next(line for line in lines if "ether " in line)
        mac_parts = mac_line.split()
        mac_address = mac_parts[1]
        # Bilgileri birleştirerek mesaj oluştur
        message = f"IP Adresi: {ip_address}\nNetmask: {netmask}\nBroadcast: {broadcast}\nMAC Adresi: {mac_address}"
        
        # Mesajı Telegram'a gönder
        bot.send_message(call.message.chat.id, message)
        sleep(1)
        homepage(bot ,call.message, "Başka ne yapmak istersiniz?")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Hata: {e}")
