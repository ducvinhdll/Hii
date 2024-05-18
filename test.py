import telebot
import requests
import time
import threading
import re
import requests
from telebot import TeleBot, types

# Thay thế bằng token của bạn
BOT_TOKEN = '7110772979:AAF0l8WM50GnTTC9GPO74_oU0-DH_Y7brTs'
bot = telebot.TeleBot(BOT_TOKEN)

# Biến lưu trữ tin nhắn tự động
auto_messages = {}

@bot.message_handler(commands=['soundcloud'])
def send_soundcloud(message):
    try:
        url_match = re.search(r'(https?://[^\s]+)', message.text)
        if url_match:
            url = url_match.group(1)

            loading_message = bot.send_message(message.chat.id, "🔎")

            api_url = f"https://thanhtien.vpndns.net/api.php?url={url}&type=04"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    bot.send_message(message.chat.id, "URL không hợp lệ.")
                    bot.delete_message(message.chat.id, loading_message.message_id)
                else:
                    title = data.get('title')
                    thoi_gian = data.get('thoi_gian')
                    size = data.get('size')
                    url_audio = data.get('url')

                    markup = types.InlineKeyboardMarkup()
                    btn_url = types.InlineKeyboardButton("🌐 Download From API ", url=url_audio)
                    markup.add(btn_url)
                    mp3_link = f"<a href=\"{url_audio}\">‏</a>"

                    bot.send_message(message.chat.id,
                                     f"╭─────⭓SoundCloud | ᴍʀ 𝐕𝐋𝐒\n"
                                     f"│»  🔔 Xin chào: @{message.from_user.username}\n"
                                     f"│»  🎶 Name: {title}\n"
                                     f"│»  🕛 Thời gian: {thoi_gian}\n"
                                     f"│»  📂 Size: {size}\n"
                                     f"╰───────────────────────\n{mp3_link}",
                                     reply_markup=markup, parse_mode="HTML")
                    bot.delete_message(message.chat.id, loading_message.message_id)
            else:
                bot.send_message(message.chat.id, "URL không hợp lệ")
                bot.delete_message(message.chat.id, loading_message.message_id)
        else:
            bot.send_message(message.chat.id, "Sử dụng: /soundcloud {url}")
            bot.delete_message(message.chat.id, loading_message.message_id)
    except Exception as e:
        print(f"Error: {e}")
        bot.delete_message(message.chat.id, loading_message.message_id)
        
        
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
    time.sleep(3600)

# Khởi tạo luồng để chạy hàm send_auto_messages
message_thread = threading.Thread(target=send_auto_messages)
message_thread.daemon = True
message_thread.start()     
        
        
# Khởi chạy bot
bot.infinity_polling(timeout=60, long_polling_timeout = 2)