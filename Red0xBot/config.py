import os
from dotenv import load_dotenv

load_dotenv()

#TO do : add typing to env variables
class Telegram:
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = str(os.getenv("API_HASH"))
    BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
    OWNER_ID = int(os.getenv("OWNER_ID", 0))
    WORKERS = int(os.getenv("WORKERS", "6"))  # 6 workers = 6 commands at once
    DATABASE_URL = str(os.getenv("DATABASE_URL"))
    UPDATES_CHANNEL = str(os.getenv("UPDATES_CHANNEL", "Telegram"))
    SESSION_NAME = str(os.getenv("SESSION_NAME", "Red0xBot"))
    FORCE_SUB_ID = os.getenv("FORCE_SUB_ID", None)
    FORCE_SUB = os.getenv("FORCE_UPDATES_CHANNEL", False)
    FORCE_SUB = True if str(FORCE_SUB).lower() == "true" else False
    SLEEP_THRESHOLD = int(os.getenv("SLEEP_THRESHOLD", 60))
    FILE_PIC = os.getenv("FILE_PIC", "https://graph.org/file/5bb9935be0229adf98b73.jpg")
    START_PIC = os.getenv("START_PIC", "https://graph.org/file/290af25276fa34fa8f0aa.jpg")
    VERIFY_PIC = os.getenv("VERIFY_PIC", "https://graph.org/file/736e21cc0efa4d8c2a0e4.jpg")
    MULTI_CLIENT: bool = False
    BOOK_CHANNEL = int(os.getenv("BOOK_CHANNEL", 0))   # Logs channel for file logs
    FLOG_CHANNEL = int(os.getenv("FLOG_CHANNEL", 0))   # Logs channel for file logs
    ULOG_CHANNEL = int(os.getenv("ULOG_CHANNEL", 0))   # Logs channel for user logs
    MODE = os.getenv("MODE", "primary")
    SECONDARY = True if MODE.lower() == "secondary" else False
    #AUTH_USERS = list(set(int(x) for x in str(os.getenv("AUTH_USERS", "")).split()))

class Server:
    PORT = int(os.getenv("PORT", 8080))
    BIND_ADDRESS = str(os.getenv("BIND_ADDRESS", "0.0.0.0"))
    PING_INTERVAL = int(os.getenv("PING_INTERVAL", "1200"))
    HAS_SSL = str(os.getenv("HAS_SSL", "0").lower()) in ("1", "true", "t", "yes", "y")
    NO_PORT = str(os.getenv("NO_PORT", "0").lower()) in ("1", "true", "t", "yes", "y")
    FQDN = str(os.getenv("FQDN", BIND_ADDRESS))
    URL = "http{}://{}{}/".format(
        "s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":" + str(PORT)
    )