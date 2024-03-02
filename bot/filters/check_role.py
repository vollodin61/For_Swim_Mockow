from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Iterable


class CheckRole(BaseFilter):
	"""Фильтр для проверки ролей пользователей админ/не админ, например
	Чтоб использовать нужно создать экземпляр класса, и передать в него список доверенных id
	check = CheckRole([])
	потом декоратором использовать можно на админских командах, например
	должен принимать в себя объект Message (лучше почитать про то, как работают фильтры))))
	check(msg)
	"""
	def __init__(self, user_ids: int | Iterable) -> None:
		self.user_ids = user_ids

	async def __call__(self, msg: Message) -> bool:
		if isinstance(self.user_ids, int):
			return msg.from_user.id == self.user_ids
		return msg.from_user.id in self.user_ids

check_role = CheckRole([])
