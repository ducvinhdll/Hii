import telebot
import time
from threading import Timer

API_TOKEN = '6670246261:AAFS3K9uioh4pmTlXW05E2tGDL4i0YMrT7U'
bot = telebot.TeleBot(API_TOKEN)

# Lưu trữ nội dung theo chat_id để gửi sau 15 phút
messages_to_send = {}

def send_later(chat_id, text):
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['addtext'])
def handle_addtext(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hãy nhập nội dung bạn muốn gửi sau 15 phút.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text
    if chat_id in messages_to_send:
        # Cập nhật nội dung và thiết lập trình hẹn giờ để gửi tin nhắn
        messages_to_send[chat_id].extend([(time.time() + 15 * 60, text)])
        bot.reply_to(message, "Nội dung của bạn đã được lưu. Tin nhắn sẽ được gửi sau 15 phút.")
    else:
        # Bắt đầu lưu trữ tin nhắn và thiết lập trình hẹn giờ
        messages_to_send[chat_id] = [(time.time() + 15 * 60, text)]
        bot.reply_to(message, "Nội dung của bạn đã được lưu. Tin nhắn sẽ được gửi sau 15 phút.")
        # Tạo một vòng lặp liên tục để gửi tin nhắn
        def send_messages_periodically():
            current_time = time.time()
            for msg_time, msg_text in messages_to_send[chat_id]:
                if current_time >= msg_time:
                    send_later(chat_id, msg_text)
                    messages_to_send[chat_id].remove((msg_time, msg_text))
            if messages_to_send[chat_id]:
                Timer(15 * 60, send_messages_periodically).start()
                
        # Bắt đầu vòng lặp lần đầu tiên
        Timer(15 * 60, send_messages_periodically).start()


@bot.message_handler(commands=['time'])
def show_uptime(message):
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'{hours} giờ, {minutes} phút, {seconds} giây'
    bot.reply_to(message, f'Bot Đã Hoạt Động Được: {uptime_str}')
    
    
bot.infinity_polling(timeout=60, long_polling_timeout = 1)