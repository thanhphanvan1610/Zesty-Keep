from utils.note_manager import find_note_by_id, create_or_update_vocabulary_note
from utils.gen_vocabulary import get_vocabulary_list
from auth import authenticate
from dotenv import load_dotenv
from database.database import add_vocabulary_to_db, get_vocabulary_from_db
import os
from utils.logger import setup_logging
import logging

setup_logging()


load_dotenv()

EMAIL = os.getenv('EMAIL')
MASTER_TOKEN = os.getenv('MASTER_TOKEN')

def new_vocabulary(note_id):
    keep = authenticate(Email=EMAIL, Master_Token=MASTER_TOKEN)
    if not keep:
        return
    
    vocab_list = get_vocabulary_list()
    if vocab_list:
        add_vocabulary_to_db(vocab_list, note_id)
        create_or_update_vocabulary_note(keep, note_id,  vocab_list)
    else:
       logging.warn("No vocabulary list obtained.")