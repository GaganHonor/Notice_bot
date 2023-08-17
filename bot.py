import os
import sys
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

ADMIN_ID = 6335120725  # Replace with your admin ID
BOT_TOKENS = ["6252912208:AAEpojCjevXkKlKRyGWivmYJRdZWegRails"]  # Rece with your bot tokens

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

            # Save the original user's chat ID and message ID for future reference
            context.user_data["original_chat_id"] = user_id
            context.user_data["original_message_id"] = update.message.message_id
        else:
            context.bot.send_message(
                chat_id=user_id,
                text=f"Sorry, {first_name} {last_name}! The server can't find your 📂 \nPlease contact the admin for assistance."
            )
            context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=update.message.message_id)
    else:
        context.bot.send_message(
            chat_id=user_id,
            text="Welcome, Admin!"
        )

def set_value_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    if user_id == ADMIN_ID:
        # Code to set a value
        pass
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

def admin_reply_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    if user_id == ADMIN_ID:
        text = update.message.text

        # Get the original user's chat ID and message ID from the forwarded message
        original_chat_id = context.user_data.get("original_chat_id")
        original_message_id = context.user_data.get("original_message_id")

        # Send the reply to the original user
        context.bot.send_message(
            chat_id=original_chat_id,
            text=text
        )

        # Update the user_data to remove the reference to the forwarded message
        del context.user_data["original_chat_id"]
        del context.user_data["original_message_id"]
    else:
        context.bot.send_message(
            chat_id=user_id,
            text="You are not authorized to use this command."
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
        admin_reply_handler = MessageHandler(Filters.text & Filters.user(ADMIN_ID), admin_reply_command)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(set_value_handler)
        dispatcher.add_handler(restart_handler)
        dispatcher.add_handler(forward_handler)
        dispatcher.add_handler(admin_reply_handler)

        updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
