from utils.logger import setup_logging
import logging

setup_logging()

def find_note_by_id(keep, note_id):
    try:
        notes = keep.all()
        note = next((note for note in notes if note.id == note_id), None)
        if note:
            logging.info(f"Found note with ID: {note_id}")
        else:
            logging.info(f"No note found with ID: {note_id}")
        return note
    except Exception as e:
        logging.error(f"Error finding note by ID: {e}")
        return None


def create_or_update_vocabulary_note(keep, note_id, vocab_list):
    try:
        note = find_note_by_id(keep, note_id)
        if note is None:
            logging.info(f"No note found with ID: {note_id}. Creating a new note.")
            note = keep.createNote('Daily Vocabulary', '')
            note_id = note.id
            logging.info(f"Created new note with ID: {note.id}")
        else:
           logging.info(f"Found existing note with ID: {note_id}")

        # Retrieve the existing vocabulary from the note
        existing_vocab = note.text.strip().split('\n') if note.text else []

        # Merge the existing vocabulary with the new vocabulary
        combined_vocab = existing_vocab + [f"{word}: {meaning}" for word, meaning in vocab_list]

        # Keep only the last 5 entries
        final_vocab = combined_vocab[-5:]

        # Update the note's text with the final vocabulary list
        note.text = "\n".join(final_vocab)
        note.save()
        
        # Synchronize changes
        keep.sync()
        
        logging.info("Vocabulary note updated successfully.")
    except Exception as e:
        logging.error(f"Error creating or updating vocabulary note: {e}")

