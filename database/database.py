import sqlite3
from utils.logger import setup_logging
import logging

setup_logging()

DB_FILE = "./database/vocabulary.db"

def initialize_db():
    """Create a SQLite database to store vocabulary if it doesn't exist."""
    logging.info("Initializing database...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS vocabulary (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      word TEXT NOT NULL,
                      meaning TEXT NOT NULL,
                      topic TEXT
                      note_id TEXT)''')
    conn.commit()
    conn.close()

def add_vocabulary_to_db(vocab_list, topic, note_id):
    """Insert vocabulary into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for word, meaning in vocab_list:
        cursor.execute("INSERT INTO vocabulary (word, meaning, topic, note_id) VALUES (?, ?, ?)", (word, meaning, topic, note_id))
    conn.commit()
    conn.close()
    logging.info("Vocabulary added to database.")

def get_vocabulary_from_db(note_id):
    """Retrieve vocabulary from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT word, meaning FROM vocabulary WHERE note_id = ?", (note_id,))
    vocab_list = cursor.fetchall()
    conn.close()
    return vocab_list

def delete_vocabulary_from_db(note_id):
    """Delete vocabulary from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vocabulary WHERE note_id = ?", (note_id,))
    conn.commit()
    conn.close()
    logging.info("Vocabulary deleted from database.")
    

def get_vocabulary_list():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT word, meaning FROM vocabulary")
    vocab_list = cursor.fetchall()
    conn.close()
    return vocab_list
       