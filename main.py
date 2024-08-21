import os
import schedule
import time
from utils.reset_new_vocabulary import new_vocabulary
from platforms.telegram_bot import TelegramBot
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TELEBOT_API") or ""
note_id = "1917557bfc1.83d789cfd8ffbe9f"    
    
def main():
    
    tele_bot = TelegramBot(bot_token, note_id)
    tele_bot.run()
    schedule.every().day.at("07:00").do(new_vocabulary(note_id))
    print("Scheduler started. Waiting for the next run...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
