import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

ACTION_URL = os.getenv('ACTION_URL')
VIDEO_URL = os.getenv('VIDEO_URL')

OPEN_JSON = {
    "name": "accessControlOpen"
    }
HEADERS = {
    "Authorization": f"Bearer {os.getenv('MYHOME_TOKEN')}"
    }