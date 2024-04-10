from aiogram import types, F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
import logging
import asyncio
import time
import subprocess

from . import localization as loc, keyboards as kb, main
from .main import FaceTracking
from .config import USER_ID


router = Router()


@router.message(Command('start'))
async def start_handler(message: Message):
    if message.from_user.id != USER_ID:
        logging.warning(f'User {message.from_user.id} was not found in the whitelist!')
        return
    await message.answer(text=loc.start_message())
    
    
@router.message(Command('open'))
async def start_handler(message: Message):
    if message.from_user.id != USER_ID:
        logging.warning(f'User {message.from_user.id} was not found in the whitelist!')
        return
    main.open_door()
    if main.open_door():
        await message.answer(text='Door opened successfully!')


@router.message(Command('snap'))
async def start_handler(message: Message):
    if message.from_user.id != USER_ID:
        logging.warning(f'User {message.from_user.id} was not found in the whitelist!')
        return
    data = main.get_image()
    file = FSInputFile(path=main.convert_image(data))
    await message.answer_photo(photo=file)
    
    
@router.message(Command('start_tracking'))
async def start_handler(message: Message):
    if message.from_user.id != USER_ID:
        logging.warning(f'User {message.from_user.id} was not found in the whitelist!')
        return
    fase_tracking = FaceTracking()
    await fase_tracking.start_tracking(message)
    
    
@router.message(Command('stop_tracking'))
async def start_handler(message: Message):
    if message.from_user.id != USER_ID:
        logging.warning(f'User {message.from_user.id} was not found in the whitelist!')
        return
    fase_tracking = FaceTracking()
    fase_tracking.stop_tracking()


@router.message(Command('set_reboot'))
async def message_handler(message: Message):
    """
    rebooting the bot on the linux server
    """
    if message.from_user.id != USER_ID:
        logging.warning(f'User {message.from_user.id} was not found in the whitelist!')
        return
    def daily_reboot():
        time_now = time.strftime("%H:%M:%S", time.localtime())
        logging.info(time_now)
        while True:
            time_now = time.strftime("%H:%M:%S", time.localtime())
            if time_now == "00:00:00":
                subprocess.run(["pm2", "restart", "bot.py"])
            
    asyncio.create_task(daily_reboot())