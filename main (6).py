import telebot
import random

bot_token = '6846053827:AAE3zZ6tqY8dOg5ucGLWd61pIuZeECLpRng'
bot = telebot.TeleBot(bot_token)

keys = []

event_rules = ''


@bot.message_handler(commands=['start'])
def methods(message):
    help_text = '''
┌───────────────────────
│»          🔔 Xin Chào 🔔
│» Bạn Ơi! Đầu Tiên Hãy Dùng lệnh /luat Để Xem Luật Event Trước Đi?!
│» Bạn hãy sử dụng lệnh /getkey để lấy key!.
│» Sau đó bạn sẽ dùng lệnh /key + key bạn đã get và gửi cho bot!.
│» Sau Đó Tôi Và Admin Sẽ Nhận Được Thông Báo từ Bạn!!!
└───────────────────────
'''
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['help_admin'])
def methods(message):
    help_text = '''
┌───────────────────────
│»          🔔 Xin Chào 🔔
│» Bạn Ơi!
│» Bạn hãy sử dụng lệnh /taokey để tạo key cho người tham gia event nào!
│» Sử dụng lệnh /random để chọn ngẫu nhiên.
│» Sử dụng lệnh /setrule để set luật Event.
│» Ví Dụ : /setrule Hi
└───────────────────────
'''
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['random'])
def handle_random(message):
    # Lấy danh sách từ tin nhắn của người dùng (bỏ qua phần /random)
    items = message.text.split()[1:]  # Loại bỏ phần "/random"
    
    if not items:
        bot.reply_to(message, "Vui lòng cung cấp một danh sách tên hoặc số cách nhau bằng dấu cách.\nVí dụ:\n/random Alice Bob Carol\n/random 5 10 15 20")
        return
    
    # Chọn ngẫu nhiên một phần tử từ danh sách
    random_item = random.choice(items)
    bot.reply_to(message, f"Tôi đã ngẫu nhiên được chọn là: {random_item}")
    


@bot.message_handler(commands=['taokey'])
def new_key(message):
    key = message.text.split()[1]
    keys.append(key)
    bot.reply_to(message, f"Key : {key}\nĐã được tạo thành công.")

@bot.message_handler(commands=['getkey'])
def get_key(message):
    if keys:
        key = keys.pop(0)
        bot.reply_to(message, f"Đây là key của bạn: {key}")
    else:
        bot.reply_to(message, "Không có key có sẵn.")


@bot.message_handler(commands=['key'])
def handle_key(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    key = message.text.split(' ')[1]  # Lấy key từ tin nhắn

    # Gửi thông báo người chơi đã nhận key
    bot.send_message(chat_id, f"Người chơi @{username} đã nhận key: {key}")

    # Gửi thông báo tới admin
    admin_chat_id = '6895557861'  # Thay đổi thành chat_id của admin
    bot.send_message(admin_chat_id, f"Người chơi @{username} đã nhận key: {key}")

    # Gửi thông báo tới nhóm
    group_chat_id = '-4282040462'  # Thay đổi thành chat_id của nhóm
    bot.send_message(group_chat_id, f"Người chơi @{username} đã nhận key: {key}")


@bot.message_handler(commands=['setrule'])
def set_event_rules(message):
    global event_rules
    event_rules = message.text.replace('/setrule ', '')
    bot.reply_to(message, "Đã thiết lập luật của sự kiện thành công!")

@bot.message_handler(commands=['luat'])
def show_event_rules(message):
    bot.reply_to(message, "Luật của sự kiện: " + event_rules)
    


bot.infinity_polling(timeout=60, long_polling_timeout = 1)