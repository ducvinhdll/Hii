import telegram 
#code này để chạy bot thêm tính năng là chạy phà phà
import telebot 
import time
import sys
import subprocess
import requests
import random
import os 
from datetime import datetime
from pyotp import TOTP
import openai
import string
import subprocess
import sqlite3
from pytube import YouTube
from gtts import gTTS
import urllib3
import json
import wget
from telebot import types
import google.generativeai as genai
urllib3.disable_warnings()

bot_token = '7212380435:AAESyeHsC-IIm-63cgL82V2W-rAcd2K-rfc'# nhập token bot

bot = telebot.TeleBot(bot_token)



# Khởi tạo một dictionary để lưu trữ các từ ngữ và câu trả lời tương ứng
keywords = {}


# Thời gian bot bắt đầu hoạt động
start_time = time.time()

# Biến toàn cục để lưu trữ tin nhắn sẽ được gửi tự động
auto_message = ''


allowed_users = []
processes = []
admins = ["6895557861", "5789810284"] # Thay thế ADMIN_ID_1 và ADMIN_ID_2 bằng ID của các Admin
proxy_update_count = 0
last_proxy_update_time = time.time()
key_dict = {}

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()
def TimeStamp():
    now = str(datetime.date.today())
    return now
def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()

def TimeStamp():
    now = str(datetime.date.today())
    return now


@bot.message_handler(commands=['start'])
def diggory(message):
    username = message.from_user.username
    diggory_chat = f'''
┌──────────⭓VIP @Louisvinh
│» 🔔 Hello: @{username}
│»  🐸 𝐵𝑜𝑡 𝐵𝑦 顶级开发商│ ᴍʀ 𝐕𝐋𝐒\│»🛌 /admin : 𝐼𝑛𝑓𝑜 𝐴𝑑𝑚𝑖𝑛.\n│»💡 /askgpt : GPT AI Bot.\n│»🤖 /cpu : check gpu,cpu...\n│»/time: check time\n│»🌐 Telegram : @Lousivinh
└─────────────────────
    '''
    sent_message = bot.send_message(message.chat.id, diggory_chat)

    time.sleep(50)


@bot.message_handler(commands=['cpu'])
def check_cpu(message):
    # Tiếp tục xử lý lệnh cpu ở đây
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    bot.reply_to(message, f'🖥 CPU Usage: {cpu_usage}%\n💾 Memory Usage: {memory_usage}%')


@bot.message_handler(commands=['time'])
def show_uptime(message):
	
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'{hours} giờ, {minutes} phút, {seconds} giây'
    
bot.reply_to(message, f'Bot Đã Hoạt Động Được: {uptime_str}')


@bot.message_handler(commands=['ask'])
def gpt(message):
  
  chat_id = message.chat.id
  genai.configure(api_key="AIzaSyBeOeuX-CxrJw0bohXfkMi9ogQurWDp66c")

  generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
  }

  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]

  model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                            generation_config=generation_config,
                              safety_settings=safety_settings)
  start_time = time.time()
  prompt_parts = message.text.split()[1:]
  prompt_parts = ' '.join(prompt_parts)

  response = model.generate_content(prompt_parts)
  end_time = time.time()
  response_time = end_time - start_time
  bot.reply_to(message, "So tiring💫")
  bot.reply_to(message, f"●━━━━━━━🌐━━━━━━━━●\n`{response.text}`\n●━━━━━━━🌐━━━━━━━━●\n status time:{response_time}\n●━━━━━━━🌐━━━━━━━━●", parse_mode="Markdown")

@bot.message_handler(commands=['admin'])
def diggory(message):
    video = random.choice(["https://files.catbox.moe/8rflr1.mp4", "https://files.catbox.moe/pk5y20.mp4", "https://files.catbox.moe/s5xsi4.mp4", "https://files.catbox.moe/ioafmk.mp4"])
    username = message.from_user.username
    diggory_chat = f'''
┌─────⭓ DEV ᴍʀ 𝐕𝐋𝐒ㅤ🧿 | BOT
│»  🔔 Xin Chào: @{username}
│»  🌐 Zalo: xxxx
│»  🌐 Telegram : @Louisvinh
└─────────────────────
    '''
    sent_message = bot.send_message(message.chat.id, diggory_chat)

    time.sleep(20)

#Tỉa soud


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


@bot.message_handler(func=lambda message: message.text.startswith('djtme'))
def invalid_command(message):
    bot.reply_to(message, 'Chưỉ gì dạ🌚🌚')
 
@bot.message_handler(func=lambda message: message.text.startswith('duma'))
def invalid_command(message):
    bot.reply_to(message, 'Con Mẹ m👉👈 ')



bot.infinity_polling(timeout=60, long_polling_timeout = 2)