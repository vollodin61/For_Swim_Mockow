from aiogram.types import BotCommand, BotCommandScopeAllChatAdministrators

"""Это непосредственно запуск в работу команд бота"""
async def set_commands(bot):
	await bot.set_my_commands([
		BotCommand(command="start", description="Начать взаимодействие"),
		BotCommand(command="help", description="Помощь"),
		BotCommand(command="site", description="Перейти на сайт Плыви Москва"),
		BotCommand(command="trainig", description="Записаться на тренировку"),
	])

"""Это пример команд админа чата/бота"""
# async def set_admin_commands(bot):
# 	await bot.set_my_commands(
# 			[
# 				BotCommand(command="add_user_product", description="Добавить пользователю продукт"),
# 				BotCommand(command="add_user", description="Добавить пользователя"),
# 				BotCommand(command="ban_user", description="Забанить пользователя"),
# 				BotCommand(command="permban_user", description="Забанить пользователя навсегда"),
# 				BotCommand(command="deactive_status", description="Деактив статус"),
# 				BotCommand(command="ask_to_delete", description="Запросил удалиться"),
# 				BotCommand(command="change_status", description="Поменять статус пользователя"),
# 			],
# 			scope=BotCommandScopeAllChatAdministrators()
# 	)