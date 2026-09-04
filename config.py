import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "VoteZenBot")

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise RuntimeError("API_ID, API_HASH and BOT_TOKEN are required")
if not OWNER_ID:
    raise RuntimeError("OWNER_ID is required")
FALLBACK_PFP_URL = os.getenv("FALLBACK_PFP_URL", "")
DB_NAME = os.getenv("DB_NAME", "votezenbot")
MAX_SAVED_CHANNELS = 5
CLEANUP_AFTER_DAYS = 4
REMINDER_MINUTES = 60
PORT = int(os.getenv("PORT", "8080"))
MAX_START_VIDEO_SECONDS = 60
# Render sets this automatically for every Web Service — no manual config
# needed there. If hosting elsewhere, set PUBLIC_URL yourself in the env.
PUBLIC_URL = (os.getenv("PUBLIC_URL") or os.getenv("RENDER_EXTERNAL_URL") or "").rstrip("/")