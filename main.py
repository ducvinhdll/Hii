import telebot
import random
import time
import threading
from datetime import datetime

# Token của bot (thay bằng token của bạn)
TOKEN = "7906830352:AAGulZjPpRm7Y9MHSVwRVcQEPG1vP14rRxs"

# Khởi tạo bot
bot = telebot.TeleBot(TOKEN)

# Danh sách cảm xúc tùy chỉnh
EMOTIONS = ["❤️", "😍", "🔥", "👍", "🎉", "😎", "🐳", "🌟"]

# Danh sách tin nhắn chúc may mắn (mở rộng)
LUCKY_MESSAGES = [
    "🍀 Chúc cả nhóm một ngày đầy may mắn, mọi việc hanh thông! 🚀",
    "🌟 Hôm nay là ngày của bạn, hãy tỏa sáng rực rỡ nhé! 💪",
    "🐞 May mắn đang gõ cửa, mở ra để nhận quà lớn nào! 😎",
    "🎲 Tung xúc xắc may mắn, bạn sẽ thắng lớn hôm nay! 🏆",
    "🌈 Cầu vồng may mắn dẫn bạn đến những điều tuyệt vời! 💖",
    "☄️ Vận may như sao băng, hãy chộp lấy ngay! ✨",
    "🍎 Một ngày ngọt ngào và may mắn đang chờ bạn! 😊",
    "🎁 Hộp quà may mắn đã mở, hãy đón nhận niềm vui! 🥳",
    "🦄 Kỳ lân may mắn mang đến phép màu cho bạn hôm nay! 🌌",
    "💰 Túi tiền may mắn đang rung, tài lộc sắp đến! 🤑",
    "🌻 Nắng mới, vận may mới, chúc bạn rực rỡ cả ngày! ☀️",
    "🎉 Bữa tiệc may mắn bắt đầu, bạn là ngôi sao chính! 🕺",
    "🍒 May mắn chín đỏ, hái ngay để tận hưởng! 😋",
    "🚀 Phi thuyền may mắn đưa bạn đến đỉnh cao thành công! 🌠",
    "🐾 Dấu chân may mắn dẫn bạn đến những cơ hội vàng! 💎",
    "🎵 Giai điệu may mắn vang lên, hãy nhảy theo nào! 🥁",
    "🍂 Gió thu mang may mắn, bạn sẽ gặp điều bất ngờ! 😍",
    "🪄 Đũa thần may mắn vẫy, mọi ước mơ thành hiện thực! 🧙",
    "🌊 Sóng may mắn dâng trào, cuốn bạn đến bến bờ vui! 🏖️",
    "🍬 Kẹo may mắn ngọt ngào, ngày mới tràn đầy năng lượng! ⚡"
]

# Danh sách từ khóa và phản hồi tùy chỉnh
CUSTOM_RESPONSES = {
    "hello": "👋 Xin chào! Rất vui thấy bạn!",
    "love": "💕 Yêu thương ngập tràn!",
    "haha": "😂 Cười xỉu luôn á!",
    "sad": "😢 Đừng buồn, có mình đây!",
    "thanks": "🙏 Cảm ơn bạn nha!",
    "good": "🌟 Tốt lắm, tiếp tục phát huy nhé!"
}

# Xử lý tin nhắn mới trong nhóm
@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.chat.type in ['group', 'supergroup']:
        text = message.text.lower()
        response = None

        # Kiểm tra từ khóa để trả lời tùy chỉnh
        for keyword, reply in CUSTOM_RESPONSES.items():
            if keyword in text:
                response = reply
                break

        # Nếu không có từ khóa, trả về cảm xúc ngẫu nhiên
        if not response:
            response = random.choice(EMOTIONS)

        # Gửi phản hồi
        bot.reply_to(
            message,
            f"@{message.from_user.username if message.from_user.username else message.from_user.first_name} {response}",
            parse_mode="Markdown"
        )

# Hàm gửi tin nhắn chúc may mắn mỗi giờ
def send_lucky_message_periodically(chat_id):
    while True:
        bot.send_message(
            chat_id,
            random.choice(LUCKY_MESSAGES),
            parse_mode="Markdown"
        )
        time.sleep(3600)  # Chờ 1 giờ (3600 giây)

# Hàm gửi tin nhắn chúc may mắn đúng giờ
def send_lucky_message_on_hour(chat_id):
    while True:
        now = datetime.now()
        # Kiểm tra nếu là đúng giờ (phút và giây gần 0)
        if now.minute == 0 and now.second < 5:
            bot.send_message(
                chat_id,
                f"⏰ *{now.hour:02d}:00* - {random.choice(LUCKY_MESSAGES)}",
                parse_mode="Markdown"
            )
            time.sleep(3600)  # Chờ đến giờ tiếp theo
        time.sleep(1)  # Kiểm tra mỗi giây

# Lưu trữ chat_id của nhóm
chat_ids = set()

# Lệnh /start để kích hoạt bot trong nhóm
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        chat_ids.add(chat_id)
        bot.reply_to(
            message,
            "🎉 *Bot đã sẵn sàng!* \n"
            "Tôi sẽ thả cảm xúc cho mỗi tin nhắn và gửi lời chúc may mắn mỗi giờ! 🍀",
            parse_mode="Markdown"
        )

        # Bắt đầu luồng gửi tin nhắn mỗi giờ
        threading.Thread(target=send_lucky_message_periodically, args=(chat_id,), daemon=True).start()
        # Bắt đầu luồng gửi tin nhắn đúng giờ
        threading.Thread(target=send_lucky_message_on_hour, args=(chat_id,), daemon=True).start()

# Chạy bot
def main():
    print("Bot đang chạy...")
    bot.infinity_polling()

if __name__ == "__main__":
    main()