import os
import schedule
import time
import threading
import asyncio
from utils.reset_new_vocabulary import new_vocabulary
from platforms.telegram_bot import TelegramBot
from dotenv import load_dotenv
from database.database import initialize_db
from utils.logger import setup_logging
import logging

setup_logging()

load_dotenv()

bot_token = os.getenv("TELEBOT_API") or ""
note_id = "1917557bfc1.83d789cfd8ffbe9f"

def start_scheduler(note_id):
    """Function to start the scheduler."""
    schedule.every().day.at("07:00").do(lambda: new_vocabulary(note_id))
    logging.info("Scheduler started. Waiting for the next run...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")
    

def run_bot(bot_token, note_id):
    """Function to run the Telegram bot with an asyncio event loop."""
    tele_bot = TelegramBot(bot_token, note_id)
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)     # Set it as the current event loop
    loop.run_until_complete(tele_bot.run())  # Run the bot

def main():
    # Initialize the database in the main thread
    initialize_db()

    # Start the Telegram bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, args=(bot_token, note_id))
    bot_thread.daemon = True
    bot_thread.start()

    # Start the scheduler in the main thread
    start_scheduler(note_id)

if __name__ == "__main__":
    main()
