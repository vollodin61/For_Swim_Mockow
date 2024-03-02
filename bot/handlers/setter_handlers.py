from aiogram import Dispatcher

from .default import def_router
from .custom import cust_router
from .admins import admin_router

"""Тут собственно обработчики сообщений (хендлеры) включаются в работу"""

def set_routers(dp: Dispatcher):
	# dp.include_router(admin_router)  # TODO включить, когда будут готовы админские команды
	dp.include_router(cust_router)
	dp.include_router(def_router)
