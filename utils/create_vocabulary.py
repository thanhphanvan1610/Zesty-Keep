from groq import Groq
from dotenv import load_dotenv
import os
from database.database import get_vocabulary_list as get_existing_vocabulary_list

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def get_vocabulary_list(topic="General", count=5, level="B1", language="Vietnamese"):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        except_words_tuples = get_existing_vocabulary_list()
        except_words = [word for word, _ in except_words_tuples]
        
        # Construct the prompt manually
        PROMPT_TEMPLATE = (
            "Only provide a list of {count} English words about the topic {topic} at the {level} level with their meanings in {language}. "
            "Do not include any introductory text, explanations, or any other content outside of the list. "
            "Ensure these words are not in the list: {except_words}. "
            "Format the response strictly as a array of tuples with word and meaning."
        )
        
        prompt = PROMPT_TEMPLATE.format(
            count=count,
            topic=topic,
            level=level,
            language=language,
            except_words=", ".join(except_words)  # Join except_words into a comma-separated string
        )
        
        # Create the completion request with the Groq API
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a professional English vocabulary tutor. "
                        "Only generate and return the list of requested vocabulary words with meanings as tuples. "
                        "Do not include any introductory phrases, explanations, or any other content. "
                        "The response must strictly adhere to the format without any extra words or phrases."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,  # Lower temperature to reduce creative deviations
            max_tokens=150,
            top_p=1,
            stream=False
        )

        # Extract the content from the completion object
        content = completion.choices[0].message.content.strip()
        vocab_list = eval(content)
        
        # Validate that the response is in the expected format
        if not all(isinstance(item, tuple) and len(item) == 2 for item in vocab_list):
            raise ValueError("Response content is not in the expected tuple format.")
        
        return vocab_list

    except Exception as e:
        print(f"Error getting vocabulary list: {e}")
        return []

