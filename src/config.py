import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

try:
    TOKEN = str(os.getenv('BOT_TOKEN'))
    ADMIN_IDS = [int(i) for i in os.getenv('BOT_ADMIN_IDS').split(',')]
    channel_username = str(os.getenv('CHANNEL_USERNAMES'))
except (ValueError, TypeError) as e:
    print(e)
