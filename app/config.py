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
if not VONAGE_API_KEY:
    raise ValueError("Missing Vonage API key.")
if not VONAGE_API_SECRET:
    raise ValueError("Missing Vonage API secret.")
if not VONAGE_NUMBER:
    raise ValueError("Missing Vonage number.")
