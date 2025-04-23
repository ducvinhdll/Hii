import time
import telebot

# Initialize the bot
bot = telebot.TeleBot('7906830352:AAGulZjPpRm7Y9MHSVwRVcQEPG1vP14rRxs')

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

# Start the bot
print("Bot is running...")
bot.polling()