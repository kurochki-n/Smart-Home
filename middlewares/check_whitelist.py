import logging
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from utils import tools


class CheckWhitelist(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        whitelist = await tools.get_whitelist()
        
        if event.from_user.id not in whitelist:
            logging.warning(f'User {event.from_user.id} was not found in the whitelist!')
            return
        return await handler(event, data)