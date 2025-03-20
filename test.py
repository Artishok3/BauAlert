import os 
from dotenv import load_dotenv

load_dotenv("shit.env")

print("BOT_TOKEN:", os.getenv("BOT_TOKEN"))
print("CHAT_ID:", os.getenv("CHAT_ID"))