from .antispam_middleware import Antispam
from .scheduler_middleware import SchedulerMiddleware
# from .check_role_middleware import CheckRoleMiddleware

from bot.data.bot_cfg import red_storage, scheduler
# from bot.data.bot_cfg import admins

"""Тут миддлвари запускаются в работу"""

def set_middleware(dp):
	# dp.update.outer_middleware.register(CheckRoleMiddleware(admins))
	dp.update.middleware.register(SchedulerMiddleware(scheduler=scheduler))
	dp.message.middleware.register(Antispam(storage=red_storage))
