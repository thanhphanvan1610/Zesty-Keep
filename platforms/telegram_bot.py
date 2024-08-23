from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    filters,
)
from utils.new_vocabulary import new_vocabulary
from database.database import delete_vocabulary_from_db
from utils.logger import setup_logging
import logging
import sys
import os

setup_logging()

TOPIC, LEVEL = range(2)

class TelegramBot:
    def __init__(self, token: str, note_id: str):
        self.token = token
        self.application = Application.builder().token(self.token).build()
        self.note_id = note_id

    async def start(self, update: Update, context: CallbackContext):
        if update.message:
            await update.message.reply_text("Hello! I'm a telegram bot to manage your notes. Send me a message to get started.")

    async def help(self, update: Update, context: CallbackContext):
        help_text = (
            "Here are the commands you can use:\n\n"
            "/start - Start interacting with the bot\n"
            "/destroy - Delete all vocabulary from the note\n"
            "/help - Show this help message\n"
            "/new - Reset and add new vocabulary to the note\n"
            "/reset - Reset the current conversation\n"
            "/stop - Stop the bot\n"
            "/restart - Restart the bot\n"
        )
        await update.message.reply_text(help_text)

    async def new_vocabulary_start(self, update: Update, context: CallbackContext):
        await update.message.reply_text("Please enter the topic for the new vocabulary.")
        return TOPIC

    async def set_topic(self, update: Update, context: CallbackContext):
        context.user_data["topic"] = update.message.text
        await update.message.reply_text(f"Topic set to {update.message.text}. Now, please enter the level (e.g., A1, B2, C1).")
        return LEVEL

    async def set_level(self, update: Update, context: CallbackContext):
        context.user_data["level"] = update.message.text
        topic = context.user_data["topic"]
        level = context.user_data["level"]

        # Call the new_vocabulary function with user-provided topic and level
        new_vocabulary(note_id=self.note_id, topic=topic, level=level)

        await update.message.reply_text(f"Vocabulary updated successfully for topic: {topic} at level: {level}.")
        return ConversationHandler.END

    async def handle_message(self, update: Update, context: CallbackContext):
        if update.message:
            await update.message.reply_text("I'm sorry, I don't understand that command. Please use /help to see the available commands.")
    
    async def delete_vocabulary(self, update: Update, context: CallbackContext):
        delete_vocabulary_from_db(self.note_id)
        await update.message.reply_text("Vocabulary deleted successfully.")
        
    async def stop(self, update: Update, context: CallbackContext):
        if update.message:
            await update.message.reply_text("Goodbye! Have a nice day!")
        return ConversationHandler.END


    def run(self):
        
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("new", self.new_vocabulary_start)],
            states={
                TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.set_topic)],
                LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.set_level)],
            },
            fallbacks=[
                CommandHandler("stop", self.stop)
            ],
        )

        # Add handlers to the application
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("destroy", self.delete_vocabulary))
        self.application.add_handler(conv_handler)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CommandHandler("stop", self.stop))
        

        logging.info("Telegram bot started.")
        self.application.run_polling()
