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

bot_token = '6554957940:AAH-bbTunSqVLxpVmVxuFVRnCnqRhax9fhY'# nhập token bot

bot = telebot.TeleBot(bot_token)

# Danh sách người dùng bị cấm
banned_users = []


warnings = {}

# Khởi tạo một dictionary để lưu trữ các từ ngữ và câu trả lời tương ứng
keywords = {}


# Thời gian bot bắt đầu hoạt động
start_time = time.time()

# Khai báo API key của OpenAI
# ID chat Telegram bạn muốn gửi tin nhắn

allowed_users = []
processes = []
ADMIN_ID = 6895557861 #id admin
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
│»  🐸 𝐵𝑜𝑡 𝐵𝑦 顶级开发商│ ᴍʀ 𝐕𝐋𝐒\│»📝 /random_face : Randomly generate sharp faces.\n│»🛌 /admin : 𝐼𝑛𝑓𝑜 𝐴𝑑𝑚𝑖𝑛.\n│»⏲️ /tt : download tiktok videos without logo.\n│»🛡️ /ytb :download Youtube videos.\n│»🖥️ /tt_fb : 检查脸书信息.\n│»💡 /askgpt : GPT AI Bot.\n│»🤖 /time: check time\n│»🌐 Telegram : @Lousivinh
└─────────────────────
    '''
    sent_message = bot.send_message(message.chat.id, diggory_chat)

    time.sleep(50)


@bot.message_handler(commands=['system'])
def speed_test(message):
    if message.from_user.id not in ADMIN_USER_IDS:
        bot.reply_to(message, "Bạn không có quyền.")
        return
    
    loading_message = bot.reply_to(message, "🔎")

    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_formatted = f"{hours}h {minutes}m {seconds}s"
    
    st = speedtest.Speedtest()
    st.download()  
    st.upload()   
    ping = st.results.ping
    download_speed = st.results.download / 1024 / 1024 
    upload_speed = st.results.upload / 1024 / 1024     
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    
    ip_info = requests.get('https://ipinfo.io/json').json()
    ip_country = ip_info.get('country', 'Unknown')
    
    api_url = 'https://thanhtien.vpndns.net/api.php'
    start_time_api = time.time()
    response = requests.get(api_url)
    api_ping_time = (time.time() - start_time_api) * 1000  # Convert to milliseconds
    
    result_message = (f"┌─────⭓ System | Mr.CS\n"
                      f"│» ⏱️ Uptime: {uptime_formatted}\n"
                      f"│» 🌐 Ping: {ping} ms\n"
                      f"│» ⤵️ Download: {download_speed:.2f} Mbps\n"
                      f"│» ⤴️ Upload: {upload_speed:.2f} Mbps\n"
                      f"│» 🖥️ CPU: {cpu_usage}%\n"
                      f"│» 🧠 Memory: {memory_usage}%\n"
                      f"│» 🛜 Country: {ip_country}\n"
                      f"│» 📡 API Ping: {api_ping_time:.2f} ms\n"
                      f"└────────────────────────")
    
    bot.reply_to(message, result_message)
    bot.delete_message(message.chat.id, loading_message.message_id)



@bot.message_handler(commands=['bansd'])
def ban_user(message):
    """
    Lệnh /bansd để cấm người dùng sử dụng tất cả các lệnh của bot.
    """
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.username

    # Kiểm tra xem người dùng đã bị cấm chưa
    if user_id in banned_users:
        bot.send_message(chat_id, f"Người dùng @{user_name} đã bị cấm.")
    else:
        # Thêm người dùng vào danh sách cấm
        banned_users.append(user_id)
        bot.send_message(chat_id, f"Người dùng @{user_name} đã bị cấm.")

@bot.message_handler(func=lambda message: message.from_user.id in banned_users)
def restrict_banned_user(message):
    """
    Hạn chế người dùng bị cấm sử dụng bot.
    """
    bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(commands=['unban'])
def unban_user(message):
    """
    Lệnh /unban để bỏ cấm người dùng.
    """
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.username

    if user_id in banned_users:
        banned_users.remove(user_id)
        bot.send_message(chat_id, f"Người dùng @{user_name} đã được bỏ cấm.")
    else:
        bot.send_message(chat_id, f"Người dùng @{user_name} không bị cấm.")


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
  bot.reply_to(message, "💫")
  bot.reply_to(message, f"●━━━━━━━🌐━━━━━━━━●\n{response.text}\n●━━━━━━━🌐━━━━━━━━●\n status time:{response_time}\n●━━━━━━━🌐━━━━━━━━●", parse_mode="Markdown")

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


        



@bot.message_handler(commands=['random_face'])
def send_random_face(message):
    sent_message = bot.send_message(message.chat.id, "Please wait for photos...")
    response = requests.get("https://thispersondoesnotexist.com/")
    
    if response.status_code == 200:
        bot.send_photo(message.chat.id, response.content)
        bot.delete_message(message.chat.id, sent_message.message_id)
    else:
        bot.reply_to(message, "Không thể lấy ảnh vào lúc này.")
        bot.delete_message(message.chat.id, sent_message.message_id)

@bot.message_handler(commands=['ytb'])
def handle_youtube(message):
	if message.text and len(message.text.split()) > 1:
		youtube = YouTube(message.text.split()[1])
		sent_message = bot.reply_to(message, f'𝑋𝑖𝑛 𝑐ℎ𝑜̛̀ 𝑚𝑜̣̂𝑡 𝑡𝑖́...!🐰\n+ 𝑇𝑖𝑒̂𝑢 𝑑𝑒̂̀: {youtube.title} \n𝑇ℎ𝑜̛̀𝑖 𝐿𝑢̛𝑜̛̣𝑛𝑔: {youtube.length} 𝐺𝑖𝑎̂𝑦\n𝐷𝑢̛𝑜̛̣𝑐 𝑇𝑎̉𝑖 𝐿𝑒̂𝑛 𝐵𝑜̛̉𝑖: {youtube.author}')
		try:
			video = youtube.streams.get_highest_resolution()
			video.download()
			bot.send_video(message.chat.id, video=open(video.default_filename, 'rb'), caption=f'𝐷𝑎̃ 𝑋𝑜𝑛𝑔 𝐶𝑎̉𝑚 𝑂̛𝑛 𝐵𝑎̣𝑛 𝐷𝑎̃ 𝐷𝑢̀𝑛𝑔❤️\n𝑇𝑖𝑒̂𝑢 𝑑𝑒̂̀: {youtube.title} \n𝑇ℎ𝑜̛̀𝑖 𝐿𝑢̛𝑜̛̣𝑛𝑔: {youtube.length} 𝐺𝑖𝑎̂𝑦\n𝐷𝑢̛𝑜̛̣𝑐 𝑇𝑎̉𝑖 𝐿𝑒̂𝑛 𝐵𝑜̛̉𝑖: {youtube.author}', reply_to_message_id=message.message_id, supports_streaming=True,timeout=3000000)
			os.remove(video.default_filename)
			bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
		except Exception as e:
			bot.reply_to(message, f'𝐷𝑎̃ 𝑋𝑎̉𝑦 𝑅𝑎 𝐿𝑜̂̃𝑖: {str(e)}')
			os.remove(video.default_filename)
	else:
		bot.reply_to(message, '𝑆𝑢̛̉ 𝐷𝑢̣𝑛𝑔: /ytb {link_video}.')
        
        
@bot.message_handler(commands=['tt'])
def luuvideo_tiktok(message):
  if len(message.text.split()) == 1:
    sent_message = bot.reply_to(message, 'Please enter link\nExample: /tt + (linkvideo)')
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
   bot.send_video(message.chat.id, video=linkz, caption=f'𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎𝚍. 𝚃𝚑𝚊𝚗𝚔 𝚢𝚘𝚞 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚐 𝚘𝚞𝚛 𝚋𝚘𝚝.\n│» Title: {tieude}\n│» Number of views: {view}\n│» 𝐴𝑑𝑚𝑖𝑛: t.me/Louisvinh', reply_to_message_id=message.message_id, supports_streaming=True)
  except Exception as e:
   bot.reply_to(message, f'Oh my God, Because the video is too heavy, you must download it using a link: {linkz}')
   bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)  


@bot.message_handler(commands=['time'])
def handle_time(message):
    # Tính toán thời gian bot đã hoạt động
    uptime = time.time() - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)

    # Lấy thông tin sử dụng CPU
    cpu_percent = psutil.cpu_percent()

    # Gửi phản hồi cho người dùng
    bot.reply_to(message, f"Bot đã hoạt động được: {hours} giờ {minutes} phút {seconds} giây\nSử dụng CPU: {cpu_percent}%")
    
@bot.message_handler(commands=['tt_fb'])
def get_facebook_info(message):
    chat_id = message.chat.id
    message_id = message.message_id
    command_parts = message.text.split(' ')
    if len(command_parts) == 1:
        bot.reply_to(message, "Sử dụng: /check_fb {url}")
        return
    url = command_parts[1]

    if url:
        sent_message = bot.send_message(chat_id, "🔎", reply_to_message_id=message_id)
        response = requests.get('https://thanhtien.vpndns.net/convertID.php?url=' + url, verify=False)
        data = response.json()
        if 'id' in data:
            user_id = data['id']
            api_url = 'https://thanhtien.vpndns.net/apiCheck.php?id=' + user_id
            response = requests.get(api_url, verify=False)
            data = response.json()
            if 'status' in data and data['status'] == 'error':
                bot.send_message(chat_id, "❌ Không tìm thấy thông tin liên quan đến link này trên Facebook.", reply_to_message_id=message_id)
            elif 'result' in data:
                formatted_data = format_user_data(data['result'])
                bot.send_message(chat_id, formatted_data, reply_to_message_id=message_id, parse_mode='HTML')
                bot.delete_message(chat_id, sent_message.message_id) 
        else:
            bot.send_message(chat_id, "❌ Vui lòng kiểm tra lại, có thể link bạn check đã sai định dạng hoặc không tồn tại trên Facebook.", reply_to_message_id=message_id)
            bot.delete_message(chat_id, sent_message.message_id) 
    else:
        bot.send_message(chat_id, "⚠️ Vui lòng nhập một ID, Facebook link, hoặc username sau /check_fb.", reply_to_message_id=message_id)
        bot.delete_message(chat_id, sent_message.message_id) 

def get_flag(language_code):
    flag_mapping = {
        'af_ZA': '🇿🇦',
        'am_ET': '🇪🇹',
        'ar_AR': '🇸🇦',
        'az_AZ': '🇦🇿',
        'be_BY': '🇧🇾',
        'bg_BG': '🇧🇬',
        'bn_IN': '🇮🇳',
        'bs_BA': '🇧🇦',
        'ca_ES': '🇪🇸',
        'cs_CZ': '🇨🇿',
        'da_DK': '🇩🇰',
        'de_DE': '🇩🇪',
        'el_GR': '🇬🇷',
        'en_GB': '🇬🇧',
        'en_PI': '🇬🇧',
        'en_UD': '🇬🇧',
        'en_US': '🇺🇸',
        'en_UD': '🇺🇸',
        'en_XA': '🇺🇸',
        'en_XL': '🇺🇸',
        'en_XA': '🇺🇸',
        'en_XA': '🇺🇸',
        'en_XA': '🇺🇸',
        'en_ZA': '🇿🇦',
        'es_CL': '🇨🇱',
        'es_CO': '🇨🇴',
        'es_ES': '🇪🇸',
        'es_LA': '🇪🇸',
        'es_MX': '🇲🇽',
        'es_VE': '🇻🇪',
        'et_EE': '🇪🇪',
        'eu_ES': '🇪🇸',
        'fa_IR': '🇮🇷',
        'fi_FI': '🇫🇮',
        'fil_PH': '🇵🇭',
        'fr_CA': '🇨🇦',
        'fr_FR': '🇫🇷',
        'gl_ES': '🇪🇸',
        'hi_IN': '🇮🇳',
        'hr_HR': '🇭🇷',
        'hu_HU': '🇭🇺',
        'hy_AM': '🇦🇲',
        'id_ID': '🇮🇩',
        'is_IS': '🇮🇸',
        'it_IT': '🇮🇹',
        'iw_IL': '🇮🇱',
        'ja_JP': '🇯🇵',
        'ka_GE': '🇬🇪',
        'kk_KZ': '🇰🇿',
        'km_KH': '🇰🇭',
        'kn_IN': '🇮🇳',
        'ko_KR': '🇰🇷',
        'ky_KG': '🇰🇬',
        'lo_LA': '🇱🇦',
        'lt_LT': '🇱🇹',
        'lv_LV': '🇱🇻',
        'mk_MK': '🇲🇰',
        'ml_IN': '🇮🇳',
        'mn_MN': '🇲🇳',
        'mr_IN': '🇮🇳',
        'ms_MY': '🇲🇾',
        'my_MM': '🇲🇲',
        'ne_NP': '🇳🇵',
        'nl_NL': '🇳🇱',
        'no_NO': '🇳🇴',
        'pl_PL': '🇵🇱',
        'pt_BR': '🇧🇷',
        'pt_PT': '🇵🇹',
        'ro_RO': '🇷🇴',
        'ru_RU': '🇷🇺',
        'si_LK': '🇱🇰',
        'sk_SK': '🇸🇰',
        'sl_SI': '🇸🇮',
        'sq_AL': '🇦🇱',
        'sr_RS': '🇷🇸',
        'sv_SE': '🇸🇪',
        'sw_KE': '🇰🇪',
        'ta_IN': '🇮🇳',
        'te_IN': '🇮🇳',
        'th_TH': '🇹🇭',
        'tr_TR': '🇹🇷',
        'uk_UA': '🇺🇦',
        'ur_PK': '🇵🇰',
        'uz_UZ': '🇺🇿',
        'vi_VN': '🇻🇳',
        'zh_CN': '🇨🇳',
        'zh_HK': '🇭🇰',
        'zh_TW': '🇹🇼',
    }
    return flag_mapping.get(language_code, '')

def format_user_data(user_data):
    id = user_data['id']
    name = user_data['name']
    username = user_data.get('username', '')
    verified = 'Đã xác minh' if user_data['is_verified'] else 'Chưa xác minh'
    avatar_url = user_data['picture']['data']['url']
    hometown = user_data.get('hometown', {}).get('name', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')
    location = user_data.get('location', {}).get('name', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')
    locale = user_data.get('locale', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')
    created_time = user_data.get('created_time', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')
    work = user_data.get('work', [{}])[0].get('employer', {}).get('name', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')
    birthday = user_data.get('birthday', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')
    gender = 'Nam' if user_data.get('gender') == 'male' else 'Nữ' if user_data.get('gender') == 'female' else 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌'
    relationship_status = user_data.get('relationship_status', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')
    followers = str(user_data.get('followers', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')) + ' người' if 'followers' in user_data else 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌'
    updated_time = user_data.get('updated_time', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')
    timezone = user_data.get('timezone', 'K‌h‌ô‌n‌g‌ ‌c‌ô‌n‌g‌ ‌k‌h‌a‌i‌')
    
    language_code = locale
    flag = get_flag(language_code)

    message = f"╭────⭓ Facebook Check │ 开发商│ᴍʀ 𝐕𝐋𝐒 🌷\n│ 𝗜𝗗: {id}\n│ 𝗡𝗮𝗺𝗲: {name}\n│ 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}\n│ 𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱: {verified}\n│ 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗧𝗶𝗺𝗲: {created_time}\n│ 𝗚𝗲𝗻𝗱𝗲𝗿: {gender}\n│ 𝗥𝗲𝗹𝗮𝘁𝗶𝗼𝗻𝘀𝗵𝗶𝗽𝘀: {relationship_status}\n│ 𝗛𝗼𝗺𝗲𝘁𝗼𝘄𝗻: {hometown}\n│ 𝗟𝗼𝗰𝗮𝘁𝗶𝗼𝗻: {location}\n│ 𝗪𝗼𝗿𝗸: {work}\n│ 𝗕𝗶𝗿𝘁𝗵𝗱𝗮𝘆: {birthday}\n│ 𝗙𝗼𝗹𝗹𝗼𝘄𝘀: {followers}\n├─────────────⭔\n│ 𝗟𝗼𝗰𝗮𝗹𝗲: {flag} {locale}\n│ 𝗨𝗽𝗱𝗮𝘁𝗲 𝗧𝗶𝗺𝗲: {updated_time}\n│ 𝗧𝗶𝗺𝗲 𝗭𝗼𝗻𝗲: GMT {timezone}\n╰─────────────⭓\n"
    image_link = f"<a href=\"{avatar_url}\"> ‏ </a>"
    message += image_link
    return message

@bot.message_handler(func=lambda message: message.text.startswith('djtme'))
def invalid_command(message):
    bot.reply_to(message, 'Chưỉ gì dạ🌚🌚')
 
@bot.message_handler(func=lambda message: message.text.startswith('duma'))
def invalid_command(message):
    bot.reply_to(message, 'Con Mẹ m👉👈 ')

# Xử lý lệnh /gpt


bot.infinity_polling(timeout=60, long_polling_timeout = 2)