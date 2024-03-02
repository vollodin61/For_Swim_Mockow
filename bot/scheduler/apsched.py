# from aiogram import Bot
# from aiogram.fsm.context import FSMContext
#
# from bot.data.bot_cfg import AvailableState as Avs


"""Это просто пример функции отправки отложенных сообщений"""


# async def send_message_3_days(tg_id: int, txt: str, bot: Bot, state: FSMContext):
# 	await bot.send_message(tg_id, text=txt)
#
# 	if await state.get_state() == Avs.fst_lesson or await state.get_state() == Avs.fst_homework:
# 		await state.set_state(Avs.snd_lesson)
# 	elif await state.get_state() == Avs.snd_lesson or await state.get_state() == Avs.snd_homework:
# 		await state.set_state(Avs.trd_lesson)
# 	return state
