from dataclasses import dataclass
from aiogram.utils.markdown import hlink, hbold
from .smiles import Emo
from bot.data.bot_cfg import VideoUrls as vu


@dataclass
class Texts:
	"""Все подряд тексты, которые отправлются в качестве ответов пользователям"""
	student_greeting = (f'Приветствую тебя! Спасибо за проявленный интерес и доверие!\n\n'
						f'Если хочешь узнать подробно, что здесь может происходить, то жми {Emo.arrow_right} /help\n')
	fst_l = f"Первый урок {Emo.big_smile}"
	help_text = (f'Вот что могу предложить в качестев помощи: {Emo.just_smile}\n\n'
				 f'У меня есть команды: /site и /training\n'
				 f'По которым ты можешь перейти на сайт или записаться на тренировку соответственно {Emo.just_smile}\n')
