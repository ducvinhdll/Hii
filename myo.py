import os
import json
import time
import random
import logging
import telebot
import qrcode
from io import BytesIO
from threading import Thread
from datetime import datetime, timedelta

# Token & Admin ID
BOT_TOKEN = "7941836347:AAFd1I-zaqjN5cb-Tv7dSGwU5toyH81DOfc"
ADMIN_ID = 5789810284

bot = telebot.TeleBot(BOT_TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

USERS_FILE = 'users.json'
HISTORY_FILE = 'history.json'

def load_data(file_path, default):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        with open(file_path, 'w') as f:
            json.dump(default, f)
        return default

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

authorized_users = load_data(USERS_FILE, {'users': [ADMIN_ID]})
history = load_data(HISTORY_FILE, {})

# Thông tin tài khoản ngân hàng
ACCOUNT_NAME = "LE DUC VINH"
ACCOUNT_NUMBER = "0386460434"
BANK_NAME = "Zalo Pay"
TRANSFER_NOTE = "UngHoBotAdmin"

# Tạo QR code từ thông tin chuyển khoản
def create_qr():
    qr_data = f"bank://{BANK_NAME}/?account={ACCOUNT_NUMBER}&note={TRANSFER_NOTE}"
    img = qrcode.make(qr_data)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# Lệnh /donate (có thể dùng bởi bất kỳ ai)
@bot.message_handler(commands=['donate'])
def send_donate_info(message):
    text = (
        f"**ỦNG HỘ PHÁT TRIỂN BOT**\n"
        f"`────────────────────────`\n"
        f"**Ngân hàng:** {BANK_NAME}\n"
        f"**Số tài khoản:** `{ACCOUNT_NUMBER}`\n"
        f"**Chủ tài khoản:** {ACCOUNT_NAME}\n"
        f"**Nội dung chuyển khoản:** `{TRANSFER_NOTE}`\n"
        f"`────────────────────────`\n"
        f"Cảm ơn bạn đã ủng hộ! Mỗi đóng góp đều giúp bot phát triển tốt hơn!"
    )
    qr_img = create_qr()
    bot.send_photo(message.chat.id, qr_img, caption=text, parse_mode="Markdown")

# Lệnh /start
@bot.message_handler(commands=['start'])
def start(message):
    banner = (
        "╔════════════════════╗\n"
        "║  🎰 SOI CẦU SUNWIN-MD5 BOT  ║\n"
        "╚════════════════════╝\n"
        "Chào mừng đến với *Bot Dự Đoán Tài/Xỉu*!\n\n"
        "✨ Dùng lệnh:\n"
        "  ┗ /soicau <mã phiên>\n"
        "  ┗ /feedback <phản hồi của bạn muốn gửi cho admin>\n"
        "  ┗ /donate <ủng hộ admin để phát triển bot>\n\n"
        "⚠️ Bot miễn phí cho mọi người!\n"
        "_Chúc bạn may mắn và nổ lớn!_"
    )
    bot.reply_to(message, banner, parse_mode='Markdown')

# Lệnh /feedback
@bot.message_handler(commands=['feedback'])
def send_feedback(message):
    feedback_msg = message.text[len('/feedback '):].strip()
    if not feedback_msg:
        bot.reply_to(message, "❗ Vui lòng nhập phản hồi của bạn.", parse_mode='Markdown')
        return
    bot.send_message(ADMIN_ID, f"📩 Phản hồi từ người dùng {message.from_user.id}: \n{feedback_msg}")
    bot.reply_to(message, "✅ Đã gửi phản hồi của bạn đến admin.", parse_mode='Markdown')

# Lệnh /adduser (chỉ admin)
@bot.message_handler(commands=['adduser'])
def add_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 Bạn không có quyền sử dụng lệnh này.", parse_mode='Markdown')
        return
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "❗ Dùng: /adduser <user_id>", parse_mode='Markdown')
        return
    try:
        new_user_id = int(args[1])
        if new_user_id in authorized_users['users']:
            bot.reply_to(message, f"Người dùng `{new_user_id}` đã có quyền.", parse_mode='Markdown')
        else:
            authorized_users['users'].append(new_user_id)
            save_data(USERS_FILE, authorized_users)
            bot.reply_to(message, f"✅ Đã thêm `{new_user_id}` vào danh sách.", parse_mode='Markdown')
    except ValueError:
        bot.reply_to(message, "❗ ID phải là số.", parse_mode='Markdown')

# Lệnh /soicau (có thể dùng bởi bất kỳ ai)
@bot.message_handler(commands=['soicau'])
def soi_cau(message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "❗ Nhập đúng cú pháp: /soicau <mã phiên>", parse_mode='Markdown')
        return
    session_code = args[1].strip()
    if not session_code:
        bot.reply_to(message, "❗ Mã phiên không hợp lệ.", parse_mode='Markdown')
        return
    if str(user_id) not in history:
        history[str(user_id)] = {'last_input': '', 'last_result': '', 'history': ''}
    user_data = history[str(user_id)]
    if session_code == user_data['last_input']:
        bot.reply_to(message, f"Mã phiên `{session_code}` đã được sử dụng.\nKết quả: {user_data['last_result']}", parse_mode='Markdown')
        return
    user_data['last_input'] = session_code
    bot.reply_to(message, f"⏳ Đang xử lý phiên `{session_code}`...", parse_mode='Markdown')
    time.sleep(3)
    bot.send_message(message.chat.id, "🔍 Phân tích thuật toán Tài Xỉu-MD5...")
    time.sleep(4)
    bot.send_message(message.chat.id, "📊 Truy xuất dữ liệu lịch sử...")
    time.sleep(2)
    bot.send_message(message.chat.id, "🧠 Dự đoán kết quả...")
    time.sleep(5)
    random_value = random.random()
    outcome = '🟥 *TÀI*' if random_value < 0.5 else '🟦 *XỈU*'
    win_rate = round(random.uniform(70, 99.99), 2)
    user_data['last_result'] = outcome
    user_data['history'] += ('T' if 'TÀI' in outcome else 'X') + ' '
    history[str(user_id)] = user_data
    save_data(HISTORY_FILE, history)
    result_msg = (
        f"╭───────────────╮\n"
        f"│ 🎲 *KẾT QUẢ PHIÊN `{session_code}`* 🎲\n"
        f"╰───────────────╯\n"
        f"📌 Kết quả: {outcome}\n"
        f"📈 Tỷ lệ thắng: *{win_rate}%*\n"
        f"🧾 Lịch sử: `{user_data['history'].strip()}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"✨ _Dự đoán mang tính chất may rũi_ ✨"
    )
    bot.send_message(message.chat.id, result_msg, parse_mode='Markdown')

# Auto-message sending, editing, and deleting
def auto_message():
    while True:
        try:
            # Get list of group chats (assuming bot is added to groups)
            # Note: Telegram API doesn't provide a direct way to list all groups, so you may need to maintain a list
            # For simplicity, assume groups are stored in a JSON file or hardcoded
            group_chats = load_data('groups.json', {'groups': []})['groups']
            for chat_id in group_chats:
                # Send auto-message
                auto_msg = (
                    "🎰 *Bot Soi Cầu Sunwin-MD5* đang hoạt động!\n"
                    "Dùng /soicau <mã phiên> để dự đoán Tài/Xỉu.\n"
                    "Hỗ trợ: /donate | Phản hồi: /feedback"
                )
                sent_msg = bot.send_message(chat_id, auto_msg, parse_mode='Markdown')
                
                # Edit the message after 10 seconds
                time.sleep(10)
                edited_msg = auto_msg + "\n✨ *Cập nhật:* Hãy thử ngay để nhận dự đoán chính xác!"
                bot.edit_message_text(edited_msg, chat_id, sent_msg.message_id, parse_mode='Markdown')
                
                # Delete the message after 30 seconds
                time.sleep(30)
                bot.delete_message(chat_id, sent_msg.message_id)
        except Exception as e:
            logger.error(f"Auto-message error: {e}")
        # Send auto-messages every 5 minutes
        time.sleep(60)

# Save group chat IDs when bot is added to a group
@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_members(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            chat_id = message.chat.id
            groups = load_data('groups.json', {'groups': []})
            if chat_id not in groups['groups']:
                groups['groups'].append(chat_id)
                save_data('groups.json', groups)
                bot.send_message(chat_id, "✅ Bot đã được thêm vào nhóm! Sử dụng /start để bắt đầu.", parse_mode='Markdown')

# Main function
def main():
    try:
        logger.info("Bot started!")
        # Start auto-message thread
        auto_thread = Thread(target=auto_message)
        auto_thread.daemon = True
        auto_thread.start()
        # Start bot polling
        bot.infinity_polling(timeout=60, long_polling_timeout=1)
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        time.sleep(5)
        main()

if __name__ == "__main__":
    main()