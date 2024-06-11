import telebot
import threading
import time

API_TOKEN = '6670246261:AAFS3K9uioh4pmTlXW05E2tGDL4i0YMrT7U'
bot = telebot.TeleBot(API_TOKEN)

# Lưu trữ nội dung mong muốn và thời gian gửi
content_queue = {}

def send_message_later(chat_id, content):
    # Chờ 15 phút
    time.sleep(900)
    bot.send_message(chat_id, content)
    # Loại bỏ nội dung đã gửi khỏi hàng đợi
    if chat_id in content_queue:
        content_queue[chat_id].remove(content)
    # Kiểm tra xem còn nội dung cần gửi không
    if content_queue.get(chat_id):
        # Thực hiện gửi nội dung tiếp theo nếu có
        next_content = content_queue[chat_id][0]
        threading.Thread(target=send_message_later, args=(chat_id, next_content)).start()

@bot.message_handler(commands=['addtext'])
def add_text(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Hãy nhập nội dung bạn muốn gửi tự động sau 15 phút.")
    bot.register_next_step_handler(msg, process_content_forwarding, chat_id)

def process_content_forwarding(message, chat_id):
    content = message.text
    if chat_id in content_queue:
        content_queue[chat_id].append(content)
    else:
        content_queue[chat_id] = [content]
        # Nếu đây là nội dung đầu tiên, bắt đầu gửi sau 15 phút
        threading.Thread(target=send_message_later, args=(chat_id, content)).start()
    bot.send_message(chat_id, "Nội dung của bạn đã được lên lịch để gửi sau 15 phút.")

if __name__ == '__main__':
    bot.infinity_polling(timeout=60, long_polling_timeout = 1)