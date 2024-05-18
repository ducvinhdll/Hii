import telebot
import requests
import time
import threading

# Thay thế bằng token của bạn
BOT_TOKEN = '7110772979:AAF0l8WM50GnTTC9GPO74_oU0-DH_Y7brTs'
bot = telebot.TeleBot(BOT_TOKEN)

# Biến lưu trữ tin nhắn tự động
auto_messages = {}

# Hàm xử lý lệnh /start
@bot.message_handler(commands=['startadmin'])
def send_welcome(message):
  bot.reply_to(message, "Xin chào! Tôi là bot tự động gửi tin nhắn. Sử dụng lệnh /setmess để thêm tin nhắn gửi tự động.")

# Hàm xử lý lệnh /setmess
@bot.message_handler(commands=['setmess'])
def set_auto_message(message):
  try:
    # Lấy nội dung tin nhắn từ người dùng
    new_message = message.text.split(' ', 1)[1]
    
    # Lưu trữ tin nhắn vào biến auto_messages
    auto_messages[message.chat.id] = new_message
    
    bot.reply_to(message, f"Tin nhắn tự động đã được cập nhật thành: {new_message}")

  except IndexError:
    bot.reply_to(message, "Vui lòng cung cấp tin nhắn sau lệnh /setmess, ví dụ: /setmess Xin chào!")

# Hàm gửi tin nhắn tự động 
def send_auto_messages():
  while True:
    for chat_id, message in auto_messages.items():
      try:
        bot.send_message(chat_id, message)
      except Exception as e:
        print(f"Lỗi khi gửi tin nhắn: {e}")

    # Đợi 1 giờ trước khi gửi lại
    time.sleep(60)

# Khởi tạo luồng để chạy hàm send_auto_messages
message_thread = threading.Thread(target=send_auto_messages)
message_thread.daemon = True
message_thread.start()

# Khởi chạy bot
bot.polling()