from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from bot.data.smiles import Emo
from bot.data.texts import Texts as Txt
from bot.data.bot_cfg import bot, admins, AvailableState as Avs, scheduler
from bot.db.sync_requests_db_postgres import SyncORM
from bot.filters.check_role import check_role
# from bot.scheduler.apsched import send_message_3_days

admin_router = Router()


@admin_router.message(F.text == "ban@")
async def ban(msg: Message, state: FSMContext):
	"""До админских команд я ещё не дошёл у себя"""
	# давайте tg_id кого забанить
	# if msg.from_user.id == 6558982323:
	await msg.answer(text="tg_id кого баним?")
	# await state.set_data(Avs.st_ban)
	# SyncORM.sync_change_status(tg_id=, "ban")
