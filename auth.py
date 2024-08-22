import gkeepapi
import os
from dotenv import load_dotenv

load_dotenv()
Email= os.getenv('EMAIL')
Master_Token = os.getenv('MASTER_TOKEN')

def authenticate():
    keep = gkeepapi.Keep()
    try:
        keep.authenticate(Email, Master_Token)
        print("Authentication successful")
        return keep
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None