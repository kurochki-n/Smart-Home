import os
import asyncio

from contextlib import suppress
from aiohttp import ClientSession
from aiogram.types import Message, FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.myhome import MyHome
from api.face_detector import recognize_face
from utils import tools
from handlers import localization as loc 


class FaceTracking(MyHome):
    
    def __init__(
        self, 
        message: Message,
        scheduler: AsyncIOScheduler,
        session: ClientSession | None = None
    ):
        self.message = message
        self.scheduler = scheduler
        self.session = session
    
    
    async def tracking(self) -> None:
        async with ClientSession() as session:
            self.session = session
            image_data, _ = await self.get_image()
            image_path = await tools.convert_image(image_data=image_data)
            known_face_encodings = await tools.get_known_faces_encodings()
            
            result, output_path = recognize_face(
                image_path=image_path,
                known_face_encodings=known_face_encodings
            )
            
            if result:
                await self.open_door()
                await self.message.answer_photo(
                    photo=FSInputFile(path=output_path),
                    caption=loc.face_is_recognized()
                )
            os.remove(path=image_path)
            os.remove(path=output_path)
    
    
    async def start(self) -> None:
        if self.scheduler.state == 1:
            await self.stop()
        self.scheduler.add_job(
            name="Tracking",
            func=self.tracking,
            trigger="interval",
            seconds=1
        )
        self.scheduler.start()
        
        
    async def stop(self) -> None:
        with suppress(asyncio.exceptions.CancelledError):
            self.scheduler.shutdown()