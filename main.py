from data import config
from middlewares.middlewares import Is_Avaible_Middleware
from db import db

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(Is_Avaible_Middleware(config.AVAIBLE_USERS))


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Рад видеть в боте\n\n"
        "Доступные команды:\n"
        "Добавить расход: 350 продукты (пример)\n"
        "Статистика за день: /today\n"
        "Статистика за месяц: /month\n"
        "5 последних трат: /expenses\n"
        "Доступные категории: /categories"
    )
    
@dp.message_handler(commands=["categories"])
async def show_categories(message: types.Message):
    await message.answer(
        "Доступные категории:\n\n" + "\n".join(db.get_categories())
    )
    
@dp.message_handler(commands=["today"])
async def today(message: types.Message):
    await message.answer("Ваши расходы за день:\n\n" + db.expenses_today(message.from_id))
    
@dp.message_handler(commands=["expenses"])
async def today(message: types.Message):
    await message.answer(db.last_expenses(message.from_id))
    
@dp.message_handler(lambda message: message.text.startswith("/del"))
async def del_expense(message: types.Message):
    await message.answer(db.delete_expense(message))
    
@dp.message_handler()
async def new_expense(message: types.Message):
    await message.answer(db.add_expence(message))


executor.start_polling(dp, skip_updates=True)