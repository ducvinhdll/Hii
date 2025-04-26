import time
from datetime import datetime
import telebot
import threading

# Initialize the bot
API_TOKEN = '7906830352:AAGulZjPpRm7Y9MHSVwRVcQEPG1vP14rRxs'
bot = telebot.TeleBot(API_TOKEN, parse_mode='Markdown')

active_chats = set()
start_time = datetime.now()  # Ghi thời điểm bot khởi động

def auto_status():
    while True:
        now = datetime.now()
        status_text = f"""```
✅ Bot vẫn Online
🤩**Hãy dùng lệnh /soi ngay nhé!**
🕒 {now.strftime('%H:%M:%S')}
📅 {now.strftime('%d/%m/%Y')}
```"""
        for chat_id in list(active_chats):
            try:
                bot.send_message(chat_id, status_text)
            except Exception as e:
                print(f"Lỗi gửi status tới {chat_id}: {e}")
        time.sleep(3600)


# Function to mimic the JavaScript hashSeed
def hash_seed(seed: str) -> int:
    hash_value = 0
    for char in seed:
        hash_value = (hash_value << 5) - hash_value + ord(char)
        hash_value |= 0  # Ensure integer
    return abs(hash_value)

# Function to predict Tài/Xỉu
def predict_taixiu(seed: str) -> str:
    dice = []
    
    for i in range(3):
        temp_seed = seed + str(i)
        hash_value = hash_seed(temp_seed)
        dice_value = (hash_value % 6) + 1
        
        # Balance logic: reduce value if sum trends toward Tài
        if i > 0 and sum(dice) + dice_value > 10:
            dice_value = max(1, dice_value - 1)
        
        dice.append(dice_value)
    
    total = sum(dice)
    result = "Tài" if total > 10 else "Xỉu"
    
    return (
        f"🎲 Xúc xắc đã dự đoán: {', '.join(map(str, dice))}\n"
        f"🍀 Tổng điểm: {total}\n"
        f"👌🏻 Kết quả nhận được là **{result}**"
    )


@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.now()
    uptime_seconds = int((now - start_time).total_seconds())
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_text = f"{hours} giờ {minutes} phút {seconds} giây" if hours else f"{minutes} phút {seconds} giây"

    formatted_time = f"""```
🧿 Thời gian hiện tại:

🕒 {now.strftime('%H:%M:%S')}
📅 {now.strftime('%d/%m/%Y')}

⏳ Bot đã online: {uptime_text}
```"""
    bot.reply_to(message, formatted_time)

# Start auto_status thread
threading.Thread(target=auto_status, daemon=True).start()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "👋 *Hi*, dưới đây là các lệnh hỗ trợ:\n\n"
        "```Vinhlexx\n"
        "🔗 `/soi `<md5 hoặc mã phiên>  - Dự đoán Tài Xỉu (miễn phí)\n"
        "```"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")


# Command handler for /predict
@bot.message_handler(commands=['soi'])
def predict(message):
    # Check if the command has one argument
    args = message.text.split()[1:]  # Get arguments after /predict
    if len(args) != 1:
        bot.reply_to(message, "Vui lòng nhập đúng định dạng: \n/soi <mã phiên hoặc id md5>")
        return
    
    seed = args[0]
    
    # Send initial message with loading animation
    sent_message = bot.reply_to(message, "🔄 Đang dự đoán...")
    
    # Simulate loading with dots
    for i in range(3):
        bot.edit_message_text(
            f"🔄 Đang dự đoán{'.' * (i + 1)}",
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id
        )
        time.sleep(0.5)
    
    # Calculate and update with the result
    try:
        result = predict_taixiu(seed)
        bot.edit_message_text(
            result,
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id,
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.edit_message_text(
            f"❌ Lỗi: {str(e)}",
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id
        )


@bot.message_handler(func=lambda message: True)
def record_active_chats(message):
    active_chats.add(message.chat.id)
    
# Start the bot
print("Bot is running...")
bot.polling()