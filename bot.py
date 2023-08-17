import os
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    context.bot.send_message(chat_id=user_id, text="Hi there!")
    context.bot.send_photo(chat_id=user_id, photo=open("image.png", "rb"))

def main():
    TOKEN = os.environ.get("BOT_TOKEN", "6252912208:AAEpojCjevXkKlKRyGWivmYJRdZWegRails")
    bot = telegram.Bot(token=TOKEN)
    updater = Updater(bot.token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start_command)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()
    
if __name__ == "__main__":
    main()
