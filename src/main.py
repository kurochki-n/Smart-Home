import requests
from aiogram.types import FSInputFile, Message
import PIL.Image as Image
import face_recognition
import logging
import asyncio
from threading import Event
from io import BytesIO

from . import localization as loc
from .config import HEADERS, ACTION_URL, OPEN_JSON, VIDEO_URL


event = Event()


def open_door() -> bool:
    result = requests.post(f'{ACTION_URL}/actions', headers=HEADERS, json=OPEN_JSON)
    if result.status_code != 200:
        logging.error(loc.open_failed(result.status_code))
        return False
    else:
        logging.info(loc.open_successfully(result.elapsed.total_seconds()))
    return True


def get_image() -> bytes:
    result = requests.get(f'{ACTION_URL}/videosnapshots', headers=HEADERS)
    if result.status_code != 200:
        logging.error(f'Failed to get an image with status code {result.status_code}')
        return None
    logging.info(f'Image received successfully in {result.elapsed.total_seconds()}sec')
    return result.content


def convert_image(image_data: bytes) -> str:
    stream = BytesIO(image_data)
    img = Image.open(stream)
    filename = 'snapshot.jpeg'
    img.save(filename, format='JPEG', quality=75)
    return filename


def get_videostream_link() -> str:
    """
    getting a video from a link (does not work)
    """
    result = requests.get(VIDEO_URL, headers=HEADERS)
    if result.status_code != 200:
        logging.error(f'Failed to get stream link with status code {result.status_code}')
        return False
    logging.info(f'Stream link received successfully in {result.elapsed.total_seconds()}sec')
    return result.json()['data']['URL']


def compare_faces(img_intercom_path: str, true_face_path: str) -> bool:
    """
    Comparing the face from the intercom with the true face
    """
    img_intercom = face_recognition.load_image_file(img_intercom_path)
    if len(face_recognition.face_locations(img_intercom)) == 0:
        return False
    img_intercom_encodings = face_recognition.face_encodings(img_intercom)[0]

    true_face = face_recognition.load_image_file(true_face_path)
    true_face_encodings = face_recognition.face_encodings(true_face)[0]

    result = face_recognition.compare_faces([img_intercom_encodings], true_face_encodings)
    if result[0]:
        return True
    return False


class FaceTracking:
    def __init__(self) -> None:
        self.true_face_path: str = 'true_face.jpeg'
        self.true_face1_path: str = '' # 'Mom.jpeg'
        self.true_face2_path: str = '' # 'Dad.jpeg'
        self.true_face3_path: str = '' # 'Grandmother.jpeg'
        self.img_intercom_path: str = ''
        
        
    async def tracking(self, message: Message) -> None:
        await message.answer(text='Face tracking has started successfully')
        
        while not event.is_set():
            if compare_faces(self.img_intercom_path, self.true_face_path):
                if open_door():
                    logging.info(f'The user {self.true_face_path.split(".")[0]} opened the entrance using his face')
                    await message.answer(text=f'The user {self.true_face_path.split(".")[0]} opened the intercom using his face')
                    await message.answer_photo(photo=FSInputFile(path=self.img_intercom_path))
            await asyncio.sleep(0.7)
            
        await message.answer(text='Face tracking ended successfully')
       
       
    async def start_tracking(self, message: Message) -> None:
        event.set()
        event.clear()
        try:
            await asyncio.create_task(self.tracking(message))
        except:
            logging.info('Tracking has ended, an unnecessary error has come out')
    
    
    def stop_tracking(self) -> None:
        event.set()
            


        
        