import telebot
import requests
import random

bot_token = '6273372932:AAGHzLRKucfRcd4m4rUPmZkKqtFrVWD5RxE'
bot = telebot.TeleBot(bot_token)

event_rules = ''

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào mừng bạn đến với bot của chúng tôi!")

@bot.message_handler(commands=['Event'])
def set_event_rules(message):
    global event_rules
    event_rules = message.text.replace('/Event ', '')
    bot.reply_to(message, "Đã thiết lập luật của sự kiện thành công!")

@bot.message_handler(commands=['luat'])
def show_event_rules(message):
    bot.reply_to(message, "Luật của sự kiện: " + event_rules)


@bot.message_handler(commands=['giveway'])
def handle_giveway(message):
    # Sinh số ngẫu nhiên từ 1 đến 200
    random_number = random.randint(1, 200)

    # Gửi thông báo cho người dùng
    bot.reply_to(message, f"Đã gửi thông tin và số {random_number} cho Admin")

    # Gửi thông báo cho admin
    admin_message = f"Người chơi: {message.from_user.username}\nFull name: {message.from_user.full_name}\nID: {message.from_user.id}\nSố chọn: {random_number}"
    bot.send_message(6895557861, admin_message)

# Thay ADMIN_CHAT_ID bằng ID của admin để bot có thể gửi thông báo cho admin
        


bot.polling()