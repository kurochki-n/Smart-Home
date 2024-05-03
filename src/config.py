import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN="6418387707:AAGZqtHqwiQolOb8_3s-UpKlln6u9I5TimQ"
HEADERS={
    "Authorization": f"Bearer {os.getenv('INTERCOM_TOKEN')}"
    }
ACTION_URL=os.getenv('ACTION_URL')
OPEN_JSON = {
    "name": "accessControlOpen"
    }
VIDEO_URL=os.getenv('VIDEO_URL')
USER_ID=int(os.getenv('USER_ID'))