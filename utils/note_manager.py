

def find_note_by_id(keep, note_id):
    try:
        # Retrieve all notes
        notes = keep.all()
        note = next((note for note in notes if note.id == note_id), None)
        if note:
            print(f"Found note with ID: {note_id}")
        else:
            print(f"No note found with ID: {note_id}")
        return note
    except Exception as e:
        print(f"Error finding note by ID: {e}")
        return None


def create_or_update_vocabulary_note(keep, note_id, vocab_list):
    try:
        note = find_note_by_id(keep, note_id)
        if note is None:
            print(f"No note found with ID: {note_id}. Creating a new note.")
            note = keep.createNote('Daily Vocabulary', '')
            note_id = note.id
            print(f"Created new note with ID: {note.id}")
        else:
            print(f"Found existing note with ID: {note_id}")

        # Convert vocabulary list to string format
        vocab_text = "\n".join([f"{word}: {meaning}" for word, meaning in vocab_list])
        
        # Update the note's text and save it
        note.text = vocab_text
        note.save()
        
        # Synchronize changes
        keep.sync()
        
        print("Vocabulary note updated successfully.")
    except Exception as e:
        print(f"Error creating or updating vocabulary note: {e}")