from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from bot.data.smiles import Emo
from bot.data.texts import Texts as Txt
from bot.data.bot_cfg import bot, admins, AvailableState as Avs, scheduler

cust_router = Router()

"""Тут кастомные обработчики входящих сообщений и команд"""

@cust_router.message(Command('site'))
async def go_to_site(msg: Message):
	builder = InlineKeyboardBuilder()
	builder.add(InlineKeyboardButton(text="Перейти на сайт", url="https://letsswim.moscow"))
	await msg.answer(text=f"Ссылка на сайт {Emo.arrow_down}", reply_markup=builder.as_markup())


@cust_router.message(Command('training'))
async def training(msg: Message):
	builder = InlineKeyboardBuilder()
	builder.add(InlineKeyboardButton(text="Записаться", url="https://n1033976.yclients.com/"))
	await msg.answer(text=f"Ссылка на сайт {Emo.arrow_down}", reply_markup=builder.as_markup())
