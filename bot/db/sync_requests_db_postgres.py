import asyncio
import re
from typing import List

import psycopg2
from aiogram.types import Message

from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
from sqlalchemy import URL, create_engine, text, insert, select, delete, update, inspect, cast, and_, func, Integer

from bot.db.db_cfg import async_engine, async_session_factory, sync_session_factory, Base, UserStatus as Us
from bot.db.models_db_postgres import User #, Product, UserProduct


class SyncORM:
	@staticmethod
	def sync_re_msg_text_to_list(msg_text: str) -> List:
		return re.findall(pattern=r"(?<=: ).+", string=msg_text)

	@staticmethod
	def sync_get_user_by_tg_id(tg_id: int) -> User | None:
		with sync_session_factory() as sess:
			try:
				kurwa_bobre: User | None = sess.query(User).filter(User.tg_id == tg_id).one()
				# print(f'{"=" * 88}\nВот твой {kurwa_bobre = }\n{"=" * 88}')
				return kurwa_bobre
			except Exception as err:
				print(f'{"!" * 88}\nОШИПКА!\n{err}\n{"!" * 88}')
				return None

	@staticmethod
	def sync_create_user_from_ifill_bot(some_list: List) -> None:
		with sync_session_factory() as sess:
			try:
				sess.add(User(tg_id=int(some_list[0]),
						  username=some_list[1],
						  status="active",
						  first_name=some_list[2],
						  last_name=some_list[3]))
			except Exception as err:
				print(f'\n\n\nНе могу создать пользователя {err = }\n\n\n')
			finally:
				sess.commit()

	# @staticmethod
	# def sync_insert_course_to_user(tg_id: int, product: str) -> None:
	# 	with sync_session_factory() as sess:
	# 		kurwa_bobre: User | None = sess.query(User).filter(User.tg_id == tg_id).one()
	# 		course: Product | None = sess.query(Product).filter(Product.name == product).one()
	# 		kurwa_bobre.products.append(course)
	# 		sess.commit()
	# 		# return print(f"{'*' * 88}\n{kurwa_bobre.username = } {kurwa_bobre.products.__sizeof__() = }\n{'*' * 88}")

	@staticmethod
	def sync_change_status(tg_id: int, new_status: str) -> None:
		with sync_session_factory() as sess:
			kurwa_bobre: User = sess.query(User).filter(User.tg_id == tg_id).one()
			kurwa_bobre.status = new_status

	@staticmethod
	def sync_check_status(tg_id: int) -> str:
		with sync_session_factory() as sess:
			kurwa_bobre: User | None = sess.query(User).filter(User.tg_id == tg_id).one()
		return kurwa_bobre.status

	@staticmethod
	def sync_check_product(tg_id: int) -> str:
		with sync_session_factory() as sess:
			kurwa_bobre: User | None = sess.query(User).filter(User.tg_id == tg_id).one()
		return kurwa_bobre.products

	@staticmethod
	def sync_get_or_create_user_from_bot(msg: Message) -> User | None:
		with sync_session_factory() as sess:
			try:
				kurwa_bobre: User | None = sess.query(User).filter(User.tg_id == msg.from_user.id).one()
				if kurwa_bobre is not None:
					return kurwa_bobre
			except Exception as err:
				print(err)
				kurwa_bobre = User(tg_id=msg.from_user.id, username=msg.from_user.username, status="active",
								   first_name=msg.from_user.first_name, last_name=msg.from_user.last_name, )
				sess.add(kurwa_bobre)
				sess.commit()
				kurwa_bobre: User | None = sess.query(User).filter(User.tg_id == msg.from_user.id).one()
				return kurwa_bobre


########################################################################################################################

async def connect_or_create():  # тут должен быть try except подключиться|создать бд
	async with async_engine.connect() as conn:
		res = await conn.execute(text("SELECT VERSION()"))
		print(f'{res.one()=}')
		await conn.commit()

async def insert_data_many():
	async with async_session_factory() as sess:
		user_volk = User(tg_id=1, username='volk', status='active', first_name='VoVo', last_name='Koko', ended_course_id=1)
		user_bobr = User(tg_id=2, username='bobre', status='banned', first_name='Bobre', last_name='Kurwa', ended_course_id=1)
		sess.add_all([user_volk, user_bobr])
		await sess.commit()


# def ins_data():
# 	with sync_session_factory() as sess:
# 		# bobre = User(tg_id=12, username='bobre')
# 		kowka = Product(name='Доброе слово для кошки')
# 		sess.add(kowka)
# 		sess.commit()


def get_user():
	with sync_session_factory() as sess:
		worder_id = 1
		bobre = sess.get(User, worder_id)
		return bobre


def select_many_data():
	with sync_session_factory() as sess:
		queryset = select(User)
		result = sess.execute(queryset)
		users = result.scalars().all()
		print(f'{users=}')


def update_data(data_id: int = 2, t_id: int = 3):
	with sync_session_factory() as sess:
		data = sess.query(User).where(User.tg_id == t_id)
		print(data)
		data.tg_id = data_id
		# data = sess.get(User, data_id)
		print(data)
		sess.commit()


def select_diff_data():
	with sync_session_factory() as sess:
		query = (select(User.username,  # первый столбец, который хотим выбрать
					   cast(func.avg(User.products), Integer).label('avg_courses'), # Тут берём второй столбец, который хотим выбрать
						# и по к нему применяем функцию (она должна быть заранее в БД объявлена,
						# пишем тип к которому хотим привести, и пишем кастомное имя столбца, чтобы нам понятно было
					   ).select_from(User).  # явное указание таблицы из которой берём данные (не обязательно, вроде бы итак понятно)
				 filter(and_(User.created_at.contains(2023),  # условия по которым выбираем
							User.products > 2),
						)
				 .group_by(User.username)  # сгруппировать по
				 .having(User.last_name)  # дополнительный фильтр для сгруппированных данных
				 )
		print(query.compile(compile_kwargs={"literal_binds": True}))  # вывод на печать красиво и понятно
		res = sess.execute(query)  # выполняем запрос и сохраняем его в переменную
		results = res.all()  # из сохранённого запроса получаем все значения
		print(results[0].avg_courses)  # берём первое значение в результатах и столбец, который мы придумали


# def join_cte_subquery_window_func(like_language: str = "Python"):
# 	with sync_session_factory() as sess:
# 		u = aliased(User)
# 		c = aliased(Product)
# 		subq = (  # Это ПОДЗАПРОС, маленькая часть
# 			select(u,
# 				   c,
# 				   c.id.label("course_id"),
# 				   func.avg(u.tg_id).over(partition_by=u.products).cast(Integer).label("Название столбца")  # Тут мы выводим среднее по столбцу, и вывод разделяем по другому столбцу
# 																						#  Потом приводим к типу Integer и называем полученный столбец
# 				   )
# 			.select_from(u)  # явное указание из какой таблицы делать выборку, НЕ ВСЕГДА нужно
# 			.join(u, u.products == c.id).subquery("helper1")  # здесь как мы соединяем полученные результаты и называем своим именем
# 		)
# 		cte = (  # Это уже большая часть запроса, в которую помещается ПОДЗАПРОС
# 			select(  # тут мы из предыдущего запроса (который сформировался, как таблица) явно указываем, какие столбцы хотим получить
# 					subq.c.course_id,
# 					subq.c.products,
# 					subq.c.tg_id,
# 					(subq.c.products-subq.c.tg_id).label("new_col")  # тут к предыдущим столбцам присераем ещё один свой
# 			)
# 			.cte("helpers2")  # Common Table Expression (CTE) — результаты запроса, которые можно использовать множество раз в других запросах
# 		)
# 		query = (  # непосредственно ЗАПРОС в который включены предыдущие части
# 			select(cte).order_by(cte.c.new_col.desc())  # тут мы пишем запрос к БД уже, в котором предыдущий СТЕ фильтруем
# 							# по убыванию по новой колонке, которую назначили перед этим в cte
# 		)
# 		res = sess.execute(query)  # выполняем запрос и сохраняем его в переменную ВОЗВРАЩАЕТ ИТЕРАТОР ПО КОТОРОМУ МОЖНО ТОЛЬКО 1 РАЗ ПРОЙТИ
# 		results = res.all()  # из сохранённого запроса получаем все значения 1 РАЗ ПРОШЛИ, БОЛЬШЕ НЕЛЬЗЯ
# 		print(results[0].avg_courses)  # берём первое значение в результатах и столбец, который мы придумали


def select_users_with_lazy_relationship():
	"""Эта хуйня (ленивая подгрузка) не работает с асинхронщиной"""
	with sync_session_factory() as sess:
		query = (
			select(User)
		)
		print(query.compile(compile_kwargs={"literal_binds": True}))
		res = sess.execute(query)
		results = res.scalars().all()
		print(results)


def select_users_with_joined_relationship():
	with sync_session_factory() as sess:
		query = (
			select(User)
			.options(joinedload(User.products))  # Здесь должно быть по столбцу со связью
		)
		# print(query.compile(compile_kwargs={"literal_binds": True}))
		res = sess.execute(query)
		results = res.unique().scalars().all()
		print(results)


def select_users_with_selectin_relationship():
	with sync_session_factory() as sess:
		query = (
			select(User)
			.options(selectinload(User.products))  # Здесь должно быть по столбцу со связью
		)
		# print(query.compile(compile_kwargs={"literal_binds": True}))
		res = sess.execute(query)
		results = res.unique().scalars().all()
		print(results)


# def select_users_with_condition_relationship_contains_eager():
# 	with sync_session_factory() as sess:
# 		query = (
# 			select(User)  # Таблицу User
# 			.join(User.products)  # слепляем с записями из таблицы Courses
# 			.options(contains_eager(User.products))  # просим Алхимию подтянуть products_id из Courses
# 			.filter(Product.name == "Доброе слово для кошки")
# 		)
# 		res = sess.execute(query)
# 		results = res.unique().scalars().all()
# 		print(results[2].username)
