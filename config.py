"""Configuration management for LG Time Deal crawler."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# LG Time Deal URL
LG_TIMEDEAL_URL = os.getenv(
    "LG_TIMEDEAL_URL",
    "https://www.lge.co.kr/benefits/exhibitions/detail-PE00385001"
)

# Priority product codes
PRIORITY_PRODUCTS = os.getenv("PRIORITY_PRODUCTS", "42C5,42C4,48C5,48C4").split(",")

# Data storage
DATA_DIR = "data"
PRODUCTS_JSON = os.path.join(DATA_DIR, "products.json")

# Scheduler configuration
SCHEDULE_HOUR = 9
SCHEDULE_MINUTE = 0

