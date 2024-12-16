import logging
from aiohttp import ClientSession
from typing import Tuple

from data.config import HEADERS, ACTION_URL, OPEN_JSON, VIDEO_URL


class MyHome(object):
    
    def __init__(self, session: ClientSession):
        self.session = session
        
        
    async def open_door(self) -> Tuple[bool, int]:
        async with self.session.post(url=f'{ACTION_URL}/actions', headers=HEADERS, json=OPEN_JSON) as response:
            if response.status != 200:
                logging.error(f'Failed to open the door with status code {response.status}')
                return False, response.status
            logging.info('Door opened successfully')
            return True, response.status


    async def get_image(self) -> Tuple[bytes | None, int]:
        async with self.session.get(url=f'{ACTION_URL}/videosnapshots', headers=HEADERS) as response:
            if response.status != 200:
                logging.error(f'Failed to get an image with status code {response.status}')
                return None, response.status
            logging.info(f'Image received successfully')
            return await response.content.read(), response.status


    async def get_videostream_link(self) -> Tuple[str | None, int]:
        async with self.session.get(url=VIDEO_URL, headers=HEADERS) as response:
            if response.status != 200:
                logging.error(f'Failed to get stream link with status code {response.status}')
                return None, response.status
            logging.info(f'Stream link received successfully')
            data = await response.json()
            return data['data']['URL'], response.status


        
        