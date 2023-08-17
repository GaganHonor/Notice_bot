import os
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
counter = 455
def start_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    if "counter" not in context.user_data:
        context.user_data["counter"] = 0
    context.user_data["counter"] += 1
    counter = context.user_data["counter"]
    context.bot.send_message(chat_id=user_id, text=f"Hi, {first_name} {last_name}! The server can't find your 📂 \n {counter}+{counter} users faced this error Today.")
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
