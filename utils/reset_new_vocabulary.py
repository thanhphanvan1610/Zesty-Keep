from utils.note_manager import find_note_by_id, create_or_update_vocabulary_note
from utils.gen_vocabulary import get_vocabulary_list
from auth import authenticate
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv('EMAIL')
MASTER_TOKEN = os.getenv('MASTER_TOKEN')

def new_vocabulary(note_id):
    keep = authenticate(Email=EMAIL, Master_Token=MASTER_TOKEN)
    if not keep:
        return

    print(find_note_by_id(keep, note_id))
    
    vocab_list = get_vocabulary_list()
    if vocab_list:
        create_or_update_vocabulary_note(keep, note_id, vocab_list)
    else:
        print("No vocabulary list obtained.")