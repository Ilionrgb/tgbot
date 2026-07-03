import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import os
from dotenv import load_dotenv
from aiogram import F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
@dp.message(Command("start"))
async def start(message: Message):
    kb = ReplyKeyboardMarkup(keyboard = [
	[KeyboardButton(text="🧮 Калькулятор")],
	[KeyboardButton(text="ℹ️ Помощь")]
    ], resize_keyboard=True)
    await message.answer(f"Привет, {message.from_user.first_name}!", reply_markup=kb)
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Я простой бот. Команды:\n/start - начать\n/help - помощь")
@dp.message(F.text == "ℹ️ Помощь")
async def help_button(message: Message):
    await message.answer("Я простой бот. Команды:\n/start - начать\n/help - помощь")
@dp.message(Command("calc"))
async def calc(message: Message):
    parts = message.text.split()
    try:
        if parts[2]=="+":
            result = float(parts[1])+float(parts[3])
        elif parts[2]=="-":
            result = float(parts[1])-float(parts[3])
        elif parts[2]=="*":
            result = float(parts[1])*float(parts[3])
        elif parts[2]=="/":
            result = float(parts[1])/float(parts[3])
        await message.answer(f'Результат - {result}')
    except ZeroDivisionError:
        await message.answer("Нельзя делить на ноль!")
    except ValueError:
        await message.answer("Введите нормальное выражение(пример: 2 + 2)")
    except IndexError:
        await message.answer("Введите полное выражение(число знак число)")
@dp.message(F.text=="🧮 Калькулятор")
async def calc_button(message: Message):
    await message.answer("Калькулятор готов!\nИспользуй команду /calc\nПример: /calc 10 + 5")
@dp.message(Command("choose"))
async def choose(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="➕", callback_data="add"),
     InlineKeyboardButton(text="➖", callback_data="sub")],
    [InlineKeyboardButton(text="✖️", callback_data="mul"),
     InlineKeyboardButton(text="➗", callback_data="div")]
    ])
    await message.answer("Выбери операцию:", reply_markup=kb)
@dp.callback_query(F.data=="add")
async def add_callback(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали сложение!")
    await callback.answer()
@dp.callback_query(F.data=="sub")
async def sub(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали вычитание!")
    await callback.answer()
@dp.callback_query(F.data=="mul")
async def mul(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали умножение!")
    await callback.answer()
@dp.callback_query(F.data=="div")
async def div(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали деление!")
    await callback.answer()
class CalcStates(StatesGroup):
    first_number = State()
    operator = State()
    second_number = State()
@dp.message(Command("dialog"))
async def dialog_start(message: Message, state: FSMContext):
    await message.answer("Введи первое число:")
    await state.set_state(CalcStates.first_number)
@dp.message(CalcStates.first_number)
async def get_first_number(message: Message, state: FSMContext):
    try:
        num = float(message.text)
        await state.update_data(first_number=num)
        await message.answer("Введи операцию (+, -, *, /):")
        await state.set_state(CalcStates.operator)
    except ValueError:
        await message.answer("Это не число! Попробуй ещё раз:")
@dp.message(CalcStates.operator)
async def get_operator(message: Message, state: FSMContext):
    znak = message.text
    await state.update_data(operator=znak)
    await message.answer("Введи второе число:")
    await state.set_state(CalcStates.second_number)
@dp.message(CalcStates.second_number)
async def get_second_number(message: Message, state: FSMContext):
    try:
        num = float(message.text)
        await state.update_data(second_number=num)
        data = await state.get_data()  # достаём все сохранённые данные
        num1 = data["first_number"]
        op = data["operator"]
        num2 = data["second_number"]
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            result = num1 / num2
        await message.answer(f"Результат: {result}")
        await state.clear()  # сбрасываем состояние, диалог завершён
    except ValueError:
        await message.answer("Это не число! Попробуй ещё раз:")
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())