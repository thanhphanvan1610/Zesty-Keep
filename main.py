import os
import asyncio
from utils.reset_new_vocabulary import new_vocabulary
from platforms.telegram_bot import TelegramBot
from dotenv import load_dotenv
from database.database import initialize_db
from utils.logger import setup_logging

setup_logging()
load_dotenv()

bot_token = os.getenv("TELEBOT_API") or os.environ.get("TELEBOT_API")
note_id = "19178354b1a.d1c0431359128b0d"

    

def run_bot(bot_token, note_id):
    """Function to run the Telegram bot with an asyncio event loop."""
    tele_bot = TelegramBot(bot_token, note_id)
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)     # Set it as the current event loop
    loop.run_until_complete(tele_bot.run())  # Run the bot

def main():
    initialize_db()
    run_bot(bot_token, note_id)
    
if __name__ == "__main__":
    main()
