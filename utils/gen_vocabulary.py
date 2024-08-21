from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
def get_vocabulary_list():
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = ("Provide a list of 5 C1 English words with their meanings in Vietnamese. "
                  "Format the response as a list of tuples with word and meaning.")

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
             messages=[
                {"role": "system", "content": "You are an expert in English vocabulary. "
                                                "Provide a list of 5 English words at the C1 level with their meanings in Vietnamese. "
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

        # Process the content to handle the correct format
        vocab_list = eval(content)  # Assuming the response is in tuple format
        if not all(isinstance(item, tuple) and len(item) == 2 for item in vocab_list):
            raise ValueError("Response content is not in the expected tuple format.")
        
        return vocab_list

    except Exception as e:
        print(f"Error getting vocabulary list: {e}")
        return []
