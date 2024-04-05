import subprocess
import platform
import os

def check_installation(package):
    """Verilen paketin yüklü olup olmadığını kontrol eder."""
    try:
        # Paketin yüklü olup olmadığını kontrol etmek için bir komut oluştur
        cmd = subprocess.Popen(["pip", "show", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Komutun çıktısını al
        output, error = cmd.communicate()
        # Çıktıda paket bilgisi varsa, paketin yüklü olduğunu göster
        if output:
            print(f"{package} is already installed.")
        # Paket bilgisi yoksa, paketin yüklü olmadığını göster
        else:
            print(f"{package} is not installed. Installing...")
            # Paketi yükle
            subprocess.call(["pip", "install", package])
    except Exception as e:
        print(f"An error occurred: {e}")

def read_requirements(file_path):
    """requirements.txt dosyasındaki paketleri okur ve bir liste olarak döndürür."""
    try:
        with open(file_path, "r") as file:
            # Her bir satırı oku ve boşlukları kaldırarak listeye ekle
            requirements = [line.strip() for line in file.readlines()]
        return requirements
    except Exception as e:
        print(f"An error occurred while reading requirements: {e}")
        return []

def main():
    # requirements.txt dosyasının yolu
    requirements_file = "requirements.txt"
    print("Checking dependencies...")
    # requirements.txt dosyasındaki paketleri oku
    packages = read_requirements(requirements_file)

    # Her bir paketi kontrol et ve gerekiyorsa yükle
    for package in packages:
        check_installation(package)

    # Ana dizini değiştir
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # İşletim sistemi türünü al
    system_type = platform.system()

    # Çalıştırılacak dosyanın yolu
    file_path = ""

    # İşletim sistemi türüne bağlı olarak dosya yolunu belirle
    if system_type == 'Linux':
        file_path = './linux/main.py'
    elif system_type == 'Windows':
        file_path = './windows/main.py'
    else:
        print("Bu işletim sistemi desteklenmiyor.")
        return
    
    print("Bot started successfully.")

    # Main dosyasını çalıştır
    os.system(f'python {file_path}')


if __name__ == "__main__":
    main()
