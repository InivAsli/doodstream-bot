import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AMAN: Ambil dari Environment Variables
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    DOODSTREAM_API_KEY = os.getenv('DOODSTREAM_API_KEY')
    ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]
    
    # Settings
    DOODSTREAM_BASE_URL = "https://doodstream.com/api"
    ITEMS_PER_PAGE = 5
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

config = Config()
