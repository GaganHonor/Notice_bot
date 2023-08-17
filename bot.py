import os
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import ChatAction
import time

BOT_TOKENS = [
    "6192019991:AAEmAim1EKTBaRXt_En1THU8MBxRA7MpnyY",
    "6252912208:AAEpojCjevXkKlKRyGWivmYJRdZWegRails"
]

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

        # Show typing animation
        context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        time.sleep(2)  # Simulate loading time

        context.bot.send_message(
            chat_id=user_id,
            text=f"Sorry, {first_name} {last_name}! The server can't find your 📂 \n {counter} users faced this Error today."
        )

        # Send the image along with the message
        context.bot.send_chat_action(chat_id=user_id, action=ChatAction.UPLOAD_PHOTO)
        time.sleep(2)  # Simulate loading time
        context.bot.send_photo(
            chat_id=user_id,
            photo=open("image.jpeg", "rb")
        )

    context.user_data["last_command"] = "start"

def main():
    for token in BOT_TOKENS:
        bot = telegram.Bot(token=token)
        updater = Updater(bot.token, use_context=True)
        dispatcher = updater.dispatcher
        start_handler = CommandHandler("start", start_command)
        dispatcher.add_handler(start_handler)
        updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
