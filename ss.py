from groq import Groq
from dotenv import load_dotenv
import os
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import OutputParserException
from database.database import get_vocabulary as get_existing_vocabulary_list

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')

# Template for generating the prompt
PROMPT_TEMPLATE = (
    "Provide {count} English words about topic {topic} at the {level} level with their meanings in {language}. "
    "Ensure these words are not in the list: {except_words}. "
    "The output should be a tuple of objects"
)

def get_vocabulary_list(topic="General", level="B1", language="Vietnamese", count=5):
    try:
        # Initialize the Groq client with the API key
        client = Groq(api_key=GROQ_API_KEY)

        # Retrieve the list of already learned vocabulary words from the database
        except_words_tuples = get_existing_vocabulary_list()  # Returns an array of learned word-meaning tuples
        except_words = [word for word, _ in except_words_tuples]  # Extract words only
        
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.invoke({"count": count, "topic": topic, "level": level, "language": language, "except_words": except_words})
        
        
        # Create the completion request with the Groq API
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional English vocabulary tutor specialized in providing vocabulary words "
                        "at varying difficulty levels, along with their meanings in the specified language. "
                        "You should ensure the words provided are relevant to the user's specified topic and "
                        "are not previously learned. Be concise and clear in your responses. Just focus on generate words. not say any thing else like { Here are {count} English words at the {count} level with their meanings in {language}} "
                    )
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
        
        # Validate the response format
        if not all(isinstance(item, dict) and 'word' in item and 'meaning' in item for item in vocab_list):
            raise ValueError("Response content is not in the expected JSON format.")

        # Convert to a list of tuples (word, meaning) if needed
        vocab_tuples = [(item['word'], item['meaning']) for item in vocab_list]
        
        return vocab_tuples

    except Exception as e:
        print(f"Error getting vocabulary list: {e}")
        return []

# Example usage
vocab_list = get_vocabulary_list(topic="Business", level="C1", language="Vietnamese", count=7)
print(vocab_list)
