import os
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    if "last_command" in context.user_data and context.user_data["last_command"] == "start":
        context.bot.send_message(
            chat_id=user_id,
            text=f"{first_name}, please refrain from spamming the /start command."
        )
    else:
        if "counter" not in context.user_data:
            context.user_data["counter"] = 9060

        context.user_data["counter"] += 1
        counter = context.user_data["counter"]

        context.bot.send_message(
            chat_id=user_id,
            text=f"Sorry, {first_name} {last_name}! The server can't find your 📂 \n {counter} users faced this Error today."
        )

        # Send the image along with the message
        context.bot.send_photo(
            chat_id=user_id,
            photo=open("image.png", "rb")
        )

    context.user_data["last_command"] = "start"

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
