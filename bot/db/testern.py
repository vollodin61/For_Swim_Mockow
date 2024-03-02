import asyncio

from bot.db.async_requests_db_postgres import AsyncORM
from bot.db.sync_requests_db_postgres import SyncORM, update_data
from bot.db.drop_db import drop_database

lst_courses = ["Сарафанка"]
