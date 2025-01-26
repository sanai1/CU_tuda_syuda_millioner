import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

import secrets


class UserInfo(StatesGroup):
    name = State()
    favorite_language = State()
    ex_age = State()


async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(UserInfo.name)
    await message.answer('Салам алейкум. Как тебя зовут?\n'
                         '/week\n'
                         '/who_cock\n'
                         '/my_command')


async def week(message: Message) -> None:
    await message.answer("52")


async def cock(message: Message) -> None:
    await message.answer("Алексей Шеманов")


async def process_name(message: Message, state: FSMContext) -> None:
    data = await state.update_data(name=message.text)
    await state.set_state(UserInfo.favorite_language)
    await message.answer(f"{data['name']}, какой у тебя любимый язык программирования?")


async def process_language(message: Message, state: FSMContext) -> None:
    data = await state.update_data(favorite_language=message.text)
    await state.set_state(UserInfo.ex_age)
    await message.answer(f"{data['name']}, какой у тебя опыт в этом языке?")


async def process_age(message: Message, state: FSMContext) -> None:
    data = await state.update_data(ex_age=message.text)
    match data["favorite_language"]:
        case "python":
            match int(data["ex_age"]):
                case 0:
                    answer = "Есть шанс бросить это дело!"
                case 1 | 2 | 3:
                    answer = "Бросай это дело и переходи на 1С"
                case 4 | 5 | 6 | 7:
                    answer = "Мы тебя потеряли"
        case "c#":
            match int(data["ex_age"]):
                case 0:
                    answer = "Ты уверене что тебе это надо?"
                case 1| 2 | 3:
                    answer = "Ты странный"
                case 4 | 5 | 6 | 7:
                    answer = "Пора лечиться"
        case "java":
            match int(data["ex_age"]):
                case 0:
                    answer = "Ты крутой"
                case 1 | 2 | 3:
                    answer = "Так держать"
                case 4 | 5 | 6 | 7:
                    answer = "Это мой любимый язык тоже!"
        case _:
            answer = "Не знаю такого языка =("
    await state.clear()
    await message.answer(answer)


async def main() -> None:
    bot_token = secrets.token_bot

    dp = Dispatcher()
    dp.message.register(start, Command("start"))
    dp.message.register(week, Command("week"))
    dp.message.register(cock, Command("who_cock"))
    dp.message.register(process_name, UserInfo.name)
    dp.message.register(process_language, UserInfo.favorite_language)
    dp.message.register(process_age, UserInfo.ex_age)

    bot = Bot(token=bot_token)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())