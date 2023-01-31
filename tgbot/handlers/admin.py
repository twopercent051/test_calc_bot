from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold



import json


async def admin_start(message: Message):
    pass



def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)


