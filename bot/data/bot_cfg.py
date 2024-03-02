import logging
import os
from dataclasses import dataclass

from aiogram import Dispatcher, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from google.oauth2.service_account import Credentials
from gspread_asyncio import AsyncioGspreadClientManager


from . redis_connection import Singleton
from . import format_text_html as fth
from . smiles import Emo

"""Глобальные переменные (которые везде в проекте используются). Говорят, что это уже моветон, а мне норм"""
env = Env()
env.read_env()
bot_token = env("TOKEN")
admins = list(map(lambda x: int(x), (env('ADMINS')).split(', ')))  # превращаем строку админов в список int
red = Singleton.get_connection(host='rediska')  # /// comment DOCKER
red_storage = RedisStorage(red)
dp = Dispatcher(storage=red_storage)
bot = Bot(token=bot_token, parse_mode="HTML")
scheduler = AsyncIOScheduler(timezone="UTC")


class AvailableState(StatesGroup):
	"""Примеры состояний пользователя"""
	can_start = State("can_start")
	not_in_list = State("not_in_list")
	fst_lesson = State("1 lesson")
	fst_homework = State("1 homework")
	snd_lesson = State("2 lesson")
	snd_homework = State("2 homework")
	trd_lesson = State("3 lesson")
	done = State("DONE")
	st_ban = State("ready_to_ban")
	st_permban = State("ready_to_permban")
	st_ask_to_delete = State("ready_to_ask_to_delete")
	st_deactive = State("ready_to_deactive")
	bad_states = (not_in_list, st_ban, st_permban, st_ask_to_delete, st_deactive)


def get_scoped_credentials(credentials, scopes):
	def prepare_credentials():
		return credentials.with_scopes(scopes)

	return prepare_credentials


# @dataclass
# class SheetParams:
# 	"""Параметры для взаимодействия с гугл-таблицами"""
# 	class Titles:
# 		"""Названия листов в таблице"""
# 		course = "Кошка"
# 		course_again = "Кошка повтор"
# 		webinar = "Вебинары"
# 		club = "Клуб"
# 		survey = "Опросы"
# 		otz = "Отзывы"
# 		sarafanka = "Сарафанка"
# 		master = "Мастер-группа"
#
# 	class Statuses:
# 		"""(опционально) Используется где-то там, для костыльно-велосипедного получения статуса пользователя"""
# 		new = "Впервые"
# 		again = "Повторно"
# 		new_member = "Вступил"
# 		resub = "Продление"
#
# 	scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
# 		"https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# 	google_credentials = Credentials.from_service_account_file(os.path.abspath("data/pyroecho.json")) # тут должен быть json с данными, которые от гугла получить надо
# 	scoped_credentials = get_scoped_credentials(google_credentials, scopes)
# 	google_client_manager = AsyncioGspreadClientManager(scoped_credentials)
#
# 	sheet_key = 'ТУТ ДОЛЖЕН БЫТЬ КЛЮЧ ОТ СЕРВИСА ГУГЛ-API https://console.cloud.google.com/'


class VideoUrls:
	"""Ссылки на видео, опциональный класс"""
	video1_url = 'https://youtu.be/JizEstXbJmo'
	video2_url = 'https://youtu.be/k-T7O9EJApo'
	video3_url = 'https://youtu.be/kAIMuI9SoU4'
	work_place_url = 'https://youtu.be/SCi6R8JQMvw'
