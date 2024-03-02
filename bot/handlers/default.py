import asyncio
import logging

from aiogram import F, Router
from aiogram.types import Message, Update
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from random import choice

from bot.data.bot_cfg import AvailableState as Avs, bot, admins
from bot.data.smiles import Emo
from bot.data.texts import Texts as Txt
from bot.db.async_requests_db_postgres import AsyncORM
from bot.db.sync_requests_db_postgres import SyncORM
from bot.db.db_cfg import UserStatus as Us

def_router = Router()

"""Тут дефолтных команд обработчики"""

@def_router.message(Command('start'))
async def cmd_start(msg: Message, state: FSMContext, bot: bot):
	logging.basicConfig(level=logging.INFO)
	await msg.reply(text=choice(["Привет!", "Привет, рад познакомиться!", "Здравствуйте!",
								 f"Привет, {msg.from_user.username}!", "Привет, рад познакомиться!", f"Здравствуйте, {msg.from_user.username}",
								 "Привет!", "Привет, рад познакомиться!", "Здравствуйте!",
								 "Привет!", f"Привет, {msg.from_user.username}, рад познакомиться!", f"Здравствуйте, рад познакомиться {Emo.big_smile}!",
								 f"Nihao!\nЛёша мой любимый тренер!{Emo.heart}\nХотя с появлением Вики я начал сомневаться{Emo.hah_nervous}"]))
	try:
		await AsyncORM.insert_user_from_bot(msg)
	except Exception as err:
		print(f"\n\n\n{err}\n\n\n")


@def_router.message(Command('help'))
async def cmd_help(msg: Message):
	await msg.answer(text=Txt.help_text)


@def_router.message()
async def echo(msg: Message, state: FSMContext, bot: bot):
	"""Это если в бот будут приходить неизвестные сообщения.
	В чатах такое не нужно, а вот если бот присылает тренировку ежедневную,
	то можно сделать автоответ на неизвестные действия"""
	pass