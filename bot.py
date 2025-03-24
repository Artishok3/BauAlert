import asyncio
import requests
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import json

load_dotenv("shit.env")

API_URL = "https://bau.amesame.rocks/bau?source=fuwawa"
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token = TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

async def commands_set(bot: Bot):
    commands = [
        BotCommand(command = "start", description = "Начать суточный мониторинг Bau"),
        BotCommand(command = "get", description = "Значение Bau сейчас"),
    ]
    await bot.set_my_commands(commands)

def previous_baus():
    try:
        with open("baus_data.json", "r") as f:
            raw = f.read().strip()
            if raw == "":
                return("Пустой файл")
            else:
                return int(raw)
        return 0
    except(FileNotFoundError, ValueError):
        return 0

def save_baus(value):
    with open("baus_data.json", "w") as f:
        f.write(str(value))

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
    current = get_baus()
    previous = int(previous_baus())
    difference = current - previous
    message = f"🕒 **На момент:** `{now}`\n🐶 **Тявкнули:** `{current}` раз."
    await bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode="Markdown")
    save_baus(current)

scheduler = AsyncIOScheduler()
scheduler.add_job(send_baus, "interval", hours = 24)

@dp.message(Command("get"))
async def get_command(message: types.message):
    now = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    current = get_baus()
    previous = int(previous_baus())
    difference = current - previous
    count = get_baus()
    save_baus(current)
    if difference != 0:
        await message.answer(

            f"🕒 **На момент:** *{now}*\n🐶" 
            f"**Тявкнули:** *{count}* раз.\n📊"
            f"**Пока ты нихуя не делал, нагавкали *{difference}* раз🖕.", parse_mode="Markdown"
            )   
    else:
        await message.answer(

            f"🕒 **На момент:** *{now}*\n🐶" 
            f"**Тявкнули:** *{count}* раз.\n📊"
            f"**Пока не гавкали😕**.", parse_mode="Markdown"
            )   
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("BAU BAU")

async def main():
    await commands_set(bot)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
