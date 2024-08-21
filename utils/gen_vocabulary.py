from groq import Groq
from dotenv import load_dotenv
import os
from database.database import get_vocabulary_list as get_existing_vocabulary_list

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def get_vocabulary_list():
    try:
        # Initialize the Groq client with the API key
        client = Groq(api_key=GROQ_API_KEY)

        # Retrieve the list of already learned vocabulary words from the database
        except_words = get_existing_vocabulary_list()  # Returns an array of learned words
        
        # Construct the prompt, including the list of words to avoid
        prompt = ("Provide a list of 5 B1-C2 English words with their meanings in Vietnamese. "
                  "Format the response as a list of tuples with word and meaning.")
        
        # Create the completion request with the Groq API
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": (f"You are an expert in English vocabulary. "
                                f"Provide a list of 5 English words at the B1-C2 level with their meanings in Vietnamese. "
                                f"Remember, you will never repeat the words {except_words} because they have already been learned. "
                                "Explain the meaning as short as possible, easy to understand, and popular. "
                                "Just list the words and meanings in a tuple format. Just respond with the words, not say anything else.")
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            stream=False
        )

        # Extract the content from the completion object
        content = completion.choices[0].message.content.strip()
        print(f"Response content: {content}")
        # Evaluate the content to convert it into a list of tuples
        vocab_list = eval(content)  # Assuming the response is in tuple format
        
        # Validate that the response is in the expected format
        if not all(isinstance(item, tuple) and len(item) == 2 for item in vocab_list):
            raise ValueError("Response content is not in the expected tuple format.")
        
        return vocab_list

    except Exception as e:
        print(f"Error getting vocabulary list: {e}")
        return []

