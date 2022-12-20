from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

class Is_Avaible_Middleware(BaseMiddleware):
    def __init__(self, avaible_users: list[str]):
        self.access_ids = avaible_users
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if message.from_id not in self.access_ids:
            await message.answer("__Вам отказано в доступе.__")
            raise CancelHandler()