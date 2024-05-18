import telebot
import requests
import time
import threading

# Thay thế bằng TOKEN của bạn
BOT_TOKEN = '7110772979:AAF0l8WM50GnTTC9GPO74_oU0-DH_Y7brTs'

bot = telebot.TeleBot(BOT_TOKEN)

# Biến toàn cục để lưu trữ tin nhắn
messages = []

# Xử lý lệnh /start
@bot.message_handler(commands=['lenhadmin'])
def send_welcome(message):
    bot.reply_to(message, "Chào mừng bạn đến với bot tự động gửi tin nhắn! Sử dụng lệnh /setmess để thêm tin nhắn.")


# Xử lý lệnh /setmess
@bot.message_handler(commands=['setmess'])
def set_message(message):
    text = message.text.replace('/setmess ', '')
    messages.append(text)
    bot.reply_to(message, f"Tin nhắn '{text}' đã được thêm vào danh sách.")

# Hàm gửi tin nhắn tự động
def send_messages_automatically():
    while True:
        for message in messages:
            for chat_id in bot.get_updates()[-1].message.chat.id:
                bot.send_message(chat_id, message)
        time.sleep(60)  # Gửi tin nhắn mỗi 60 giây

# Tạo luồng riêng biệt cho việc gửi tin nhắn tự động
thread = threading.Thread(target=send_messages_automatically)
thread.start()

# Bắt đầu bot
bot.infinity_polling(timeout=60, long_polling_timeout = 4)