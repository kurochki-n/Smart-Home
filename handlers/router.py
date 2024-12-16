import os
import aiohttp

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import localization as loc
from api.myhome import MyHome
from api.face_tracking import FaceTracking
from api.face_detector import recognize_face
from utils import tools



router = Router()


@router.message(Command('start'))
async def start_handler(message: Message) -> None:
    await message.answer(text=loc.start_message())
    
    
@router.message(Command('open'))
async def open_handler(message: Message) -> None:
    async with aiohttp.ClientSession() as session:
        myhome = MyHome(session=session)
        result, status = await myhome.open_door()
        image_data, _ = await myhome.get_image()
        
        if not result:
            await message.answer(text=loc.open_failed(status_code=status))
            return
        
        if image_data is None:
            await message.answer(text=loc.open_successfully())
            return
        
        image_path = await tools.convert_image(image_data=image_data)
        _, output_path = recognize_face(
            image_path=image_path,
            known_face_encodings=await tools.get_known_faces_encodings()
        )
        await message.answer_photo(
            photo=FSInputFile(path=output_path),
            caption=loc.open_successfully()
        )
        os.remove(path=image_path)
        os.remove(path=output_path)


@router.message(Command('snap'))
async def snap_handler(message: Message) -> None:
    async with aiohttp.ClientSession() as session:
        myhome = MyHome(session=session)
        image_data, status = await myhome.get_image()

        if image_data is None:
            await message.answer(text=loc.snap_failed(status_code=status))
            return
        
        image_path = await tools.convert_image(image_data=image_data)
        _, output_path = recognize_face(
            image_path=image_path,
            known_face_encodings=await tools.get_known_faces_encodings()
        )
        await message.answer_photo(photo=FSInputFile(path=output_path))
        os.remove(path=image_path)
        os.remove(path=output_path)
    
    
@router.message(Command('start_tracking'))
async def start_tracking_handler(message: Message, scheduler: AsyncIOScheduler) -> None:
    tracking = FaceTracking(message=message, scheduler=scheduler)
    await tracking.start()
    await message.answer(text=loc.tracking_started())
    
    
@router.message(Command('stop_tracking'))
async def stop_tracking_handler(message: Message, scheduler: AsyncIOScheduler) -> None:
    tracking = FaceTracking(message=message, scheduler=scheduler)
    await tracking.stop()
    await message.answer(text=loc.tracking_stopped())