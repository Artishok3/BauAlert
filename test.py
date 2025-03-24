import asyncio
import requests
import os
import json
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

load_dotenv("shit.env")

API_URL = "https://bau.amesame.rocks/bau?source=fuwawa"
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token = TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

USER_DATA = "user_data.json"

def load_users():
    with open(USER_DATA, "r") as f:
        return json.load(f)
    return {}    

def write_user_id(data):
    with open(USER_DATA, "w") as f:
        json.dump(data, f, indent = 4, ensure_ascii=False)
    print("json обновлен")

@dp.message(Command("get"))
async def get_command(message: types.message):
    user_id = str(message.from_user.id)
    users = load_users()
    
    if user_id in users:
        users[user_id]['count'] += 1
    else:
        users[user_id] = {
            'user_id' : user_id,
            'count' : 1
        }
    write_user_id(users)
    print("User appended")
    await message.answer(f"Записан {user_id}. Запросы: {users[user_id]["count"]}")
    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())