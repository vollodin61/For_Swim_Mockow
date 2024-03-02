import asyncio
import logging
import os
import sys

from bot.data.bot_cfg import bot, dp, scheduler, red_storage
from bot.db.async_requests_db_postgres import AsyncORM
from bot.db.drop_db import sync_create_database, drop_database
from bot.handlers.setter_handlers import set_routers
from bot.middlewares.set_middlewares import set_middleware
from bot.utils.bot_commands import set_commands #, set_admin_commands

sys.path.insert(1, os.path.join(sys.path[0], '..'))


async def main():
	# logging.basicConfig(level=logging.DEBUG)
	# await drop_database()  # /// comment вроде бы не надо это, но пусть поживёт тут
	sync_create_database()
	# try:
	await AsyncORM.create_models()
	# except Exception as err:
	# 	print(f"{'^^^' * 18}\nНе получилось создать бд\n{err}")
	scheduler.start()
	await set_commands(bot)
	# await set_admin_commands(bot)  /// comment раскомментить, когда создам админские команды
	await bot.delete_webhook(drop_pending_updates=True)
	set_middleware(dp)
	set_routers(dp)
	await dp.start_polling(bot)


if __name__ == "__main__":
	# try:  # /// раскоментить перед запуском
	asyncio.run(main())
	# except Exception as err:  # /// раскоментить перед запуском
	# 	print(f'Что-то пошло не так, ошибка:\n{err}')  # /// раскоментить перед запуском
