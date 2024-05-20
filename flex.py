from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    update.message.reply_text(f"│»Hi {user.first_name}\n│»You: {user.id}.\n»Welcome to Vinh Louis's new event.\n│»Please send me the /give command and the number")

def give(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    command = update.message.text.split()
    if len(command) != 2 or not command[1].isdigit() or int(command[1]) < 1 or int(command[1]) > 100:
        update.message.reply_text("Vui lòng nhập số 1 đến 100 ")
    else:
        update.message.reply_text("Thank you for participating, please wait for notification from the administrator")
        admin_message = f"Username: {user.username}, Fullname: {user.full_name}, ID: {user.id}, Number: {command[1]}"
        # Send admin_message to administrator

def main() -> None:
    updater = Updater("6273372932:AAGHzLRKucfRcd4m4rUPmZkKqtFrVWD5RxE")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.command & Filters.regex(r'^/give'), give))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()