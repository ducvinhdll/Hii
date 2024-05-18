import telebot
import time
import requests

# Thay thế YOUR_BOT_TOKEN bằng token của bot Telegram của bạn
BOT_TOKEN = '7110772979:AAF0l8WM50GnTTC9GPO74_oU0-DH_Y7brTs'

bot = telebot.TeleBot(BOT_TOKEN)

# Biến toàn cục để lưu trữ tin nhắn sẽ được gửi tự động
auto_message = ''

# Xử lý lệnh /start
@bot.message_handler(commands=['startadmin'])
def send_welcome(message):
    bot.reply_to(message, "Chào mừng bạn đến với bot gửi tin nhắn tự động! Sử dụng lệnh /setmess để cài đặt tin nhắn.")

# Xử lý lệnh /setmess
@bot.message_handler(commands=['setmess'])
def set_message(message):
    global auto_message
    auto_message = message.text.replace("/setmess ", "")
    bot.reply_to(message, f"Tin nhắn tự động đã được đặt thành:\n{auto_message}")

# Hàm gửi tin nhắn tự động sau mỗi 1 tiếng
def send_auto_message():
    while True:
        # Kiểm tra xem đã có tin nhắn tự động hay chưa
        if auto_message:
            # Lấy ID của nhóm từ tin nhắn
            chat_id = message.chat.id

            # Gửi tin nhắn tự động đến nhóm
            bot.send_message(chat_id, auto_message)

        # Dừng 1 tiếng
        time.sleep(3600)

# Chạy hàm gửi tin nhắn tự động trong một luồng riêng biệt
if __name__ == '__main__':
    # Khởi tạo luồng cho hàm send_auto_message
    import threading
    message_thread = threading.Thread(target=send_auto_message)
    message_thread.daemon = True
    message_thread.start()

    # Bắt đầu polling cho bot
bot.infinity_polling(timeout=60, long_polling_timeout = 2)