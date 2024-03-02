from typing import Dict, Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerMiddleware(BaseMiddleware):
	"""Это клёвая штука для возможности боту самому отправлять отложенные сообщения"""
	def __init__(self, scheduler: AsyncIOScheduler):
		# super().__init__()
		self._scheduler = scheduler

	async def __call__(self,
						handler: Callable[[TelegramObject, Dict[str, Any]],
						Awaitable[Any]],
						event: TelegramObject,
						data: Dict[str, Any]) -> Any:
		data["apscheduler"] = self._scheduler
		return await handler(event, data)
