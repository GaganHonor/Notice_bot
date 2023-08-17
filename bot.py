import os
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import ChatAction
import time

BOT_TOKENS = [
    "6252912208:AAEpojCjevXkKlKRyGWivmYJRdZWegRails"
]

ADMIN_ID = "6335120725"

def start_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    if user_id != ADMIN_ID:
        if "last_command" in context.user_data and context.user_data["last_command"] == "start":
            context.bot.send_message(
                chat_id=user_id,
                text=f"{first_name}, please refrain from spamming the /start command."
            )
            context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=update.message.message_id)
        else:
            context.bot.send_message(
                chat_id=user_id,
                text=f"Sorry, {first_name} {last_name}! The server can't find your 📂 \nPlease contact the admin for assistance."
            )
            context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=update.message.message_id)
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

def set_value_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    if user_id == ADMIN_ID:
        text = update.message.text
        input_value = text.split()[1]

        # Update the value of the variable
        context.user_data["counter"] = int(input_value)

        context.bot.send_message(
            chat_id=user_id,
            text=f"The value has been updated to {input_value}."
        )
    else:
        context.bot.send_message(
            chat_id=user_id,
            text="You are not authorized to use this command."
        )

def restart_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    if user_id == ADMIN_ID:
        context.bot.send_message(
            chat_id=user_id,
            text="Restarting the bot..."
        )

        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        context.bot.send_message(
            chat_id=user_id,
            text="You are not authorized to use this command."
        )

def forward_message_to_user(update: Update, context: CallbackContext):
    user_id = ADMIN_ID
    message = update.message.reply_to_message
    forward_from_id = message.forward_from.id
    forward_text = message.text

    context.bot.send_message(
        chat_id=forward_from_id,
        text=f"Admin message: {forward_text}"
    )

def main():
    for token in BOT_TOKENS:
        bot = telegram.Bot(token=token)
        updater = Updater(bot.token, use_context=True)
        dispatcher = updater.dispatcher
        start_handler = CommandHandler("start", start_command)
        set_value_handler = CommandHandler("setvalue", set_value_command)
        restart_handler = CommandHandler("restart", restart_command)
        forward_handler = MessageHandler(Filters.reply & Filters.user(ADMIN_ID), forward_message_to_user)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(set_value_handler)
        dispatcher.add_handler(restart_handler)
        dispatcher.add_handler(forward_handler)
        updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
