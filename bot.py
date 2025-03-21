import asyncio
import requests
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

load_dotenv("shit.env")

API_URL = "https://bau.amesame.rocks/bau?source=fuwawa"
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token = TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

def get_baus():

    HEADERS = { "User-Agent": "Mozilla/5.0",
        "Referer": "https://fwmcbaubau.com/",
        "Accept": "application/json",
    }
    response = requests.get(API_URL, headers=HEADERS)

    if response.status_code == 200:
        baus = response.json()["baus"]
        
    else:
        print("No response", response.status_code)
    return baus
async def send_baus():
    now = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    baus_count = get_baus()
    message = f"🕒 **На момент:** `{now}`\n🐶 **Тявкнули:** `{baus_count}` раз."
    await bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode="Markdown")

scheduler = AsyncIOScheduler()
scheduler.add_job(send_baus, "interval", seconds = 10)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("BAU BAU")

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())