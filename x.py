import time
import telebot
import requests
from io import BytesIO

# Initialize the bot
bot = telebot.TeleBot('6813833583:AAGqlSfhPZbux6237Kmpn2G_LDv-aiXxD_s')

# Image URL
IMAGE_URL = "https://i.ibb.co/8LmtK2w/unnamed.png"

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
        f"🎲 **Xúc xắc đã dự đoán**: {', '.join(map(str, dice))}\n"
        f"🍀 **Tổng điểm**: {total}\n"
        f"👑 **Kết quả đã định**: **{result}**\n"
        f"💸 Chúc bạn may mắn và thắng lớn! 🎉"
    )

# Command handler for /soi
@bot.message_handler(commands=['soi1'])
def predict(message):
    # Check if the command has one argument
    args = message.text.split()[1:]  # Get arguments after /soi
    if len(args) != 1:
        bot.reply_to(message, "📌 Vui lòng nhập đúng định dạng: \n/soi <mã phiên hoặc id md5>")
        return
    
    seed = args[0]
    
    # Send initial message with loading animation
    sent_message = bot.reply_to(message, "⚡️ **VIP Prediction Engine** khởi động...")
    
    # Simulate loading with dynamic animation
    animations = ["⚡️ Dự Đoán.", "⚡️ Dự Đoán..", "⚡️ Dự Đoán...", "⚡Dự Đoán...."]
    for anim in animations:
        bot.edit_message_text(
            anim,
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id
        )
        time.sleep(0.5)
    
    # Calculate and send the result with image
    try:
        # Fetch the image
        response = requests.get(IMAGE_URL)
        if response.status_code != 200:
            raise Exception("Không thể tải hình ảnh😭")
        
        # Send the image
        bot.send_photo(
            chat_id=sent_message.chat.id,
            photo=BytesIO(response.content),
            caption="✨ **Kết quả dự đoán đã định** ✨"
        )
        
        # Send the prediction result
        result = predict_taixiu(seed)
        bot.send_message(
            chat_id=sent_message.chat.id,
            text=result,
            parse_mode="Markdown"
        )
        
        # Delete the loading message
        bot.delete_message(
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id
        )
        
    except Exception as e:
        bot.edit_message_text(
            f"❌ **Lỗi VIP**: {str(e)}",
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id
        )

# Start the bot
print("VIP Bot is running...")
bot.polling()