from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from utils.reset_new_vocabulary import new_vocabulary
from utils.logger import setup_logging
import logging

setup_logging()

class TelegramBot:
    def __init__(self, token: str, note_id: str):
        self.token = token
        self.application = Application.builder().token(self.token).build()
        self.note_id = note_id

    async def start(self, update: Update, context: CallbackContext):
        if update.message:
            await update.message.reply_text("Hello! I'm telegram bot to manage your notes. Send me a message to get started.")

    async def help(self, update: Update, context: CallbackContext):
        help_text = (
                "Here are the commands you can use:\n\n"
                "/start - Start interacting with the bot\n"
                "/help - Show this help message\n"
                "/new - Reset and add new vocabulary to the note\n"
                "/stop - Stop the bot\n\n"
            )
        
        await update.message.reply_text(help_text)

    async def new_vocabulary(self, update: Update, context: CallbackContext):
        if update.message:
            new_vocabulary(self.note_id)
            await update.message.reply_text("Update vocabulary successful!.")
            
    async def handle_message(self, update: Update, context: CallbackContext):
        if update.message:
            await update.message.reply_text("I'm sorry, I don't understand that command. Please use /help to see the available commands.")
            
    
    async def stop(self, update: Update, context: CallbackContext):
       if update.message:
            await update.message.reply_text("Good bye! Have a nice day!.")

    def run(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("new", self.new_vocabulary))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CommandHandler("stop", self.stop))

        logging.info("Telegram bot started.")
        self.application.run_polling()
