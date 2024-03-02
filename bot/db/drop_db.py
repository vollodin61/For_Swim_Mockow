import asyncio

import asyncpg
import psycopg2


async def drop_database():
	# conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="127.0.0.1")  # /// comment
	conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="db_host", port=5432)  # /// comment  DOCKER
	cursor = conn.cursor()

	conn.autocommit = True
	# команда для создания базы данных metanit
	sql = "DROP DATABASE database"

	# выполняем код sql
	try:
		cursor.execute(sql)
		print("База данных успешно уничтожена")
	except Exception as err:
		print(err)
	cursor.close()
	conn.close()


def sync_create_database():
	# conn = psycopg2.connect(dbname="postgres", user="postgres", password="123456", host="127.0.0.1")  # /// comment  ЛОкАЛ
	conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="db_host")  # /// comment  DOCKER
	# conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port=5433)  # /// comment  DOCKER
	cursor = conn.cursor()

	conn.autocommit = True
	# команда для создания базы данных database
	sql = "CREATE DATABASE database"

	# выполняем код sql
	try:
		cursor.execute(sql)
		print("База данных успешно создана")
	except Exception as err:
		print(err)
	cursor.close()
	conn.close()
