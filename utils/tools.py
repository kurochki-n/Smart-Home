import aiofiles
import json

from typing import List


async def convert_image(image_data: bytes) -> str:
    filename = 'temp/snapshot.jpeg'
    async with aiofiles.open(filename, mode='wb') as file:
        await file.write(image_data)
    return filename


async def get_whitelist() -> List[int]:
    async with aiofiles.open('data/json/whitelist.json', mode='r') as file:
        data = await file.read()
        return json.loads(data)['whitelist']
    
    
async def get_known_faces_encodings() -> List[List[int]]:
    async with aiofiles.open('data/json/known_faces.json', mode='r') as file:
        data = await file.read()
        return json.loads(data)['face_encodings']