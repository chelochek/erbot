# python bot
from logging import shutdown

import sqlite3
import messages
import keyboards
import utils
from utils import Test
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, emoji

from config import TOKEN, ADMIN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def process_start(message: types.message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT chat_id FROM users WHERE chat_id = {message.from_user.id}")
    user = cursor.fetchall()
    if len(user) == 0:
        cursor.execute(f"INSERT INTO users(chat_id, username) values ({message.from_user.id}, '{message.from_user.username}')")
    conn.commit()
    conn.close()
    await message.reply(messages.GREETS_MSG, reply=False, parse_mode='HTML', reply_markup=keyboards.GREETS_KB)


@dp.message_handler()
async def process_text(message: types.message):
    switch = message.text.lower()
    if switch == "ссылка" and message.from_user.id == ADMIN:
        await message.reply("Введи новую ссылку")
        await dp.current_state(user=ADMIN).set_state(utils.ChangeLink.all()[0])
    elif switch == "текущая" and message.from_user.id == ADMIN:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT link FROM admin WHERE user_id = {message.from_user.id}")
        link = cursor.fetchall()[0][0]
        conn.close()
        await message.reply(f"Текущая ссылка: {link}")
    elif switch == "пройти тест":
        await message.reply(emoji.emojize(messages.TEST_MSG), reply=False)
        await message.reply("Вопрос 1: ", reply=False, reply_markup=keyboards.QUEST_1)
        await bot.send_photo(message.from_user.id, "https://sun9-7.userapi.com/impg/N3W4HBzfWvM_DQE-pWl9PfUvzI9k3etkCmqPfQ/BaTDdSQH35k.jpg?size=512x384&quality=96&sign=1b5681d1a2ff815831ae450b10ad11d7&type=album")
        await dp.current_state(user=message.from_user.id).set_state(Test.all()[0])
    elif switch == "информация":
        await message.reply(emoji.emojize("Скины будут отправлены в течении двух дней после добавления в друзья! :white_check_mark:"))
        await dp.current_state(user=ADMIN).reset_state()


@dp.message_handler(state=utils.ChangeLink.CHANGE_0)
async def process_text(message: types.message):
    await dp.current_state(user=ADMIN).reset_state()
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE admin SET link='{message.text}' WHERE user_id={ADMIN}")
    conn.commit()
    conn.close()
    await message.reply(reply=False, text="Успешно")

@dp.message_handler(state=Test.TEST_0)
async def process_text(message: types.message):
    await message.reply(emoji.emojize("NICE :white_check_mark: \n\nВопрос 2: "), reply=False, reply_markup=keyboards.QUEST_2)
    await bot.send_photo(message.from_user.id, "https://sun9-49.userapi.com/impg/MObWiwuTvAW2M7PQxiKgtewRIc3WgZ9PoT3h9g/SSK-Sxw2IpI.jpg?size=512x384&quality=96&sign=7b933c41e9aa72dac88ab775f1ff908f&type=album")
    await dp.current_state(user=message.from_user.id).set_state(Test.all()[1])


@dp.message_handler(state=Test.TEST_1)
async def process_text(message: types.message):
    await message.reply(emoji.emojize("NICE :white_check_mark: \n\nВопрос 3: "), reply=False, reply_markup=keyboards.QUEST_3)
    await bot.send_photo(message.from_user.id, "https://sun9-70.userapi.com/impg/pYDueXbKbgz16Pv5rUxPa8sAt29CGBE_ektfEQ/0H8GU9Fc3sY.jpg?size=512x384&quality=96&sign=41570bd2e975db18cedb49b60913c161&type=album")
    await dp.current_state(user=message.from_user.id).set_state(Test.all()[2])


@dp.message_handler(state=Test.TEST_2)
async def process_text(message: types.message):
    await message.reply(emoji.emojize("NICE :white_check_mark:"), reply=False, reply_markup=keyboards.END_KB)
    await dp.current_state(user=message.from_user.id).set_state(Test.all()[3])


@dp.message_handler(state=Test.TEST_3)
async def process_text(message: types.message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT link FROM admin WHERE user_id = {ADMIN}")
    link = cursor.fetchall()[0][0]
    conn.close()
    await message.reply(emoji.emojize("Добавляй бота в друзья и в течении двух дней скины будут отправлены!\n\n"
                                      f"{link}"), reply=False, reply_markup=keyboards.END_KEYB)
    await dp.current_state(user=message.from_user.id).reset_state()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
