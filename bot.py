import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "8879073327:AAHAJVZdk8fbg4MsHPSHI6o4cSyMwMUWDQk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Я простой бот. Команды:\n/start - начать\n/help - помощь")

@dp.message(Command("calc"))
async def calc(message: Message):
    parts = message.text.split()
    if parts[2]=="+":
        result = float(parts[1])+float(parts[3])
    elif parts[2]=="-":
        result = float(parts[1])-float(parts[3])
    elif parts[2]=="*":
        result = float(parts[1])*float(parts[3])
    elif parts[2]=="/":
        result = float(parts[1])/float(parts[3])
    await message.answer(f'Результат - {result}')
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
