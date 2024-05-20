import telebot
import random

# Thay đổi token của bot telegram của bạn ở đây
TOKEN = '6273372932:AAGHzLRKucfRcd4m4rUPmZkKqtFrVWD5RxE''
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    username = message.from_user.username
    bot.reply_to(message, f'Xin chào {username}!\nHãy sử sụng lệnh /give + số ngẫu nhiên của bạn từ 1-100.»Bot By ᴍʀ 𝐕𝐋𝐒ㅤ🧿')

@bot.message_handler(commands=['give'])
def handle_give(message):
    number = random.randint(1, 100)
    username = message.from_user.username
    fullname = message.from_user.first_name + ' ' + message.from_user.last_name
    bot.reply_to(message, 'Cảm ơn bạn đã tham gia!')
    bot.send_message(6895557861, f'Username: {username}\nFullname: {fullname}\nNumber chosen: {number}')

bot.infinity_polling(timeout=60, long_polling_timeout = 1)