import gkeepapi
from dotenv import load_dotenv
import os
import schedule
import time
from groq import Groq

# Load environment variables
load_dotenv()

EMAIL = 'thanhphanvan1610@gmail.com'
MASTER_TOKEN = os.getenv('MASTER_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def authenticate():
    keep = gkeepapi.Keep()
    try:
        keep.authenticate(EMAIL, MASTER_TOKEN)
        print("Authentication successful")
        return keep
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

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
            note = keep.createNote('Daily Vocabulary', '')  # Create with a default title
            note_id = note.id  # Update note_id to the new note's ID
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

def get_vocabulary_list():
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = ("Provide a list of 5 B1 English words with their meanings in Vietnamese. "
                  "Format the response as a list of tuples with word and meaning.")

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
             messages=[
                {"role": "system", "content": "You are an expert in English vocabulary. "
                                                "Provide a list of 5 English words at the B1 level with their meanings in Vietnamese. "
                                                "explain the meaning as short as possible, easy to understand, and popular"
                                                "Just list the words and meanings in a tuple format. just reponse word not say anything else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            stream=False
        )

        # Extract the content from the completion object
        content = completion.choices[0].message.content.strip()
        print(f"Response from Groq: \n{content}")

        # Process the content to handle the correct format
        vocab_list = eval(content)  # Assuming the response is in tuple format
        if not all(isinstance(item, tuple) and len(item) == 2 for item in vocab_list):
            raise ValueError("Response content is not in the expected tuple format.")
        
        return vocab_list

    except Exception as e:
        print(f"Error getting vocabulary list: {e}")
        return []

def job():
    keep = authenticate()
    if not keep:
        return

    # ID of the note you want to update
    note_id = "1917557bfc1.83d789cfd8ffbe9f"
    print(find_note_by_id(keep, note_id))
    
    vocab_list = get_vocabulary_list()
    if vocab_list:
        create_or_update_vocabulary_note(keep, note_id, vocab_list)
    else:
        print("No vocabulary list obtained.")

def main():
    job()
    
    # schedule.every().day.at("07:00").do(job)
    # print("Scheduler started. Waiting for the next run...")
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)  # wait one minute

if __name__ == "__main__":
    main()
