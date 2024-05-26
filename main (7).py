import telebot
import json
import random

API_TOKEN = '6846053827:AAE3zZ6tqY8dOg5ucGLWd61pIuZeECLpRng'  # Thay YOUR_API_TOKEN_HERE bằng token của bạn

bot = telebot.TeleBot(API_TOKEN)

# Hàm để load dữ liệu từ file
def load_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Hàm để lưu dữ liệu vào file
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

# Lệnh /register
@bot.message_handler(commands=['register'])
def register(message):
    user_id = str(message.from_user.id)
    user_data = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }
    data = load_data()
    if user_id not in data:
        data[user_id] = user_data
        save_data(data)
        bot.reply_to(message, "Bạn đã được đăng ký thành công!")
    else:
        bot.reply_to(message, "Bạn đã đăng ký trước đó rồi!")

# Tạo lệnh từ /1 đến /10
for i in range(1, 11):
    @bot.message_handler(commands=[str(i)])
    def handle_random_commands(message):
        command = message.text[1:]  # Lấy ra lệnh mà không có ký tự '/'
        result_type = random.choice(["loại", "an toàn"])
        bot.reply_to(message, f"Kết quả của lệnh /{command}: {result_type}")

# Khởi động bot
bot.polling()