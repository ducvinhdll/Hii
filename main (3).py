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

bot_token = '7110772979:AAF0l8WM50GnTTC9GPO74_oU0-DH_Y7brTs'# nhập token bot

bot = telebot.TeleBot(bot_token)

# Danh sách người dùng bị cấm
banned_users = []


warnings = {}

# Khởi tạo một dictionary để lưu trữ các từ ngữ và câu trả lời tương ứng
keywords = {}

muted_users = []

# Thời gian bot bắt đầu hoạt động
start_time = time.time()

# Khai báo API key của OpenAI
# ID chat Telegram bạn muốn gửi tin nhắn

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

# ID chat 

# Tin nhắn bạn muốn gửi


@bot.message_handler(commands=['start'])
def diggory(message):
    username = message.from_user.username
    diggory_chat = f'''
┌──────────⭓VIP ᴍʀ 𝐕𝐋𝐒ㅤ🧿
│» 🔔 Hello: @{username}
│»  🐸 𝐵𝑜𝑡 𝐵𝑦 顶级开发商│ ᴍʀ 𝐕𝐋𝐒\│»│»🛌 /admin : 𝐼𝑛𝑓𝑜 𝐴𝑑𝑚𝑖𝑛.\n│»💡 /askgpt : GPT AI Bot.\n│»🤖 /cpu : check gpu,cpu...\n│»🌐 Telegram : @Lousivinh
└─────────────────────
    '''
    sent_message = bot.send_message(message.chat.id, diggory_chat)

    time.sleep(50)


@bot.message_handler(commands=['cpu'])
def check_cpu(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    # Tiếp tục xử lý lệnh cpu ở đây
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    bot.reply_to(message, f'🖥 CPU Usage: {cpu_usage}%\n💾 Memory Usage: {memory_usage}%')


@bot.message_handler(commands=['muteuser'])
def mute_user(message):
    if str(message.from_user.id) in admins:
        user_id = message.reply_to_message.from_user.id
        muted_users.append(user_id)
        bot.reply_to(message, f"User {user_id} has been muted.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

@bot.message_handler(commands=['unuser'])
def unmute_user(message):
    if str(message.from_user.id) in admins:
        user_id = message.reply_to_message.from_user.id
        if user_id in muted_users:
            muted_users.remove(user_id)
            bot.reply_to(message, f"User {user_id} has been unmuted.")
        else:
            bot.reply_to(message, f"User {user_id} is not muted.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

@bot.message_handler(func=lambda message: message.from_user.id in muted_users)
def handle_muted_user(message):
    bot.reply_to(message, "You are muted and cannot send messages.")



@bot.message_handler(commands=['askgpt'])
def gpt(message):
  
  chat_id = message.chat.id
  genai.configure(api_key="AIzaSyDrABsaV-gGS7pmDcBBySO8uCcc2NMIzWE")

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
│»  🌐 Zalo: 0386460434
│»  🌐 Facebook: ducvinhdll
│»  🌐 Telegram : @Louisvinh
└─────────────────────
    '''
    sent_message = bot.send_message(message.chat.id, diggory_chat)

    time.sleep(20)

#Tỉa soud


        





@bot.message_handler(func=lambda message: message.text.startswith('djtme'))
def invalid_command(message):
    bot.reply_to(message, 'Chưỉ gì dạ🌚🌚')
 
@bot.message_handler(func=lambda message: message.text.startswith('duma'))
def invalid_command(message):
    bot.reply_to(message, 'Con Mẹ m👉👈 ')

# Xử lý lệnh /gpt


bot.infinity_polling(timeout=60, long_polling_timeout = 2)