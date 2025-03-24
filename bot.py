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
#
def load_users():
    with open(USER_DATA, "r") as f:
        return json.load(f)
    return {}    

def write_user_id(data):
    with open(USER_DATA, "w") as f:
        json.dump(data, f, indent = 4, ensure_ascii=False)
    print("json обновлен")


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
    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)
    users = load_users()
    
    now = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    current = get_baus()
    count = get_baus()

    if user_id in users:
        previous = users[user_id].get('prev_baus')
    
        users[user_id]['baus'] = current
        users[user_id]['prev_baus'] = previous
        users[user_id]['user_name'] = user_name
        users[user_id]['count'] += 1

        difference = current - previous
        users[user_id]['prev_baus'] = current

    else:
        users[user_id] = {
            'baus' : count,
            'user_name' : user_name,
            'user_id' : user_id,
            'count' : 1
        }
    write_user_id(users)

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
