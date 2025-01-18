import os
from dotenv import load_dotenv

load_dotenv()
# Ensure the log directory exists
LOG_DIR = "app/log"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

DATABASE_URL = "sqlite+aiosqlite:///./vonage_call_recording.db"
LOG_FILE = os.path.join(LOG_DIR, "file_{time}.log")

# Vonage API credentials
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_NUMBER = os.getenv("VONAGE_NUMBER")

# Validate Vonage environment variables
if not all([VONAGE_API_KEY, VONAGE_API_SECRET, VONAGE_NUMBER]):
    raise ValueError("Missing Vonage environment variables.")