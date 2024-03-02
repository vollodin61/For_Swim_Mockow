from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import URL, create_engine, func

from bot.data.bot_cfg import env
from bot.data.smiles import Emo

#  Alembic не удаляет колонки enum, чтобы удалилось добавить в downgrade метод миграции op.execute("DROP TYPE")
#  для красиового форматирования миграций добавил либу black, /// comment в alembic.ini раскомментировать строки 72-75
IP = env("IP")
PGUSER = env("PGUSER")
PGPASS = env("PGPASS")
DBNAME = env("DBNAME")
PGHOST = env("PGHOST")
PGPORT = env("PGPORT")
PGHOSTDOCKER = env("PGHOSTDOCKER")
PGPORTDOCKER = env("PGPORTDOCKER")


class UserStatus:
	active = "active"  # какие ещё могут быть статусы?
	deactivated_text = (f"Эта учётная запись была деактивирована {Emo.confused}\n\n"
						f"Чтобы узнать причину, исправить это, свяжись, пожалуйста, с @good_cat_admin")
	ban_text = (f"Эта учётная запись была забанена {Emo.confused}\n\n"
				f"Чтобы узнать причину, исправить это, свяжись, пожалуйста, с @good_cat_admin")
	permban_text = (f"Эта учётная запись была перманентно забанена {Emo.confused}\n\n"
					f"Чтобы узнать причину можешь связаться с @good_cat_admin\n")
	ask_to_delete_text = ("По просьбе пользователя, эта учётная запись была удалена. Хотите вернуться?\n"
						  "Напишите @good_cat_admin он знает, что делать в таких ситуациях")
	ask_to_delete_text_to_admin = "Пользователь, который просил удалиться стучит в Сарафанку"
	text_to_status = {
		'deactivated': deactivated_text,
		'ban': ban_text,
		'permban': permban_text,
		'ask_to_delete': ask_to_delete_text,
	}
	all_bad = ["deactivated", "ban", "permban", "ask_to_delete"]


class Settings:
	IP: str = env('IP')
	PGUSER: str = env('PGUSER')
	PGPASS: str = env('PGPASS')
	DBNAME: str = env('DBNAME')
	PGHOST: str = env('PGHOST')
	PGPORT: str = env('PGPORT')
	PGHOSTDOCKER: str = env('PGHOSTDOCKER')
	PGPORTDOCKER: str = env('PGPORTDOCKER')

	@property
	def local_url_asyncpg(self):
		return f'postgresql+asyncpg://{self.PGUSER}:{self.PGPASS}@{self.PGHOST}:{self.PGPORT}/{self.DBNAME}'

	@property
	def docker_url_asyncpg(self):
		return f'postgresql+asyncpg://{self.PGUSER}:{self.PGPASS}@{self.PGHOSTDOCKER}:{self.PGPORTDOCKER}/{self.DBNAME}'

	@property
	def local_url_psycopg2(self):
		return f'postgresql+psycopg2://{self.PGUSER}:{self.PGPASS}@{self.PGHOST}:{self.PGPORT}/{self.DBNAME}'

	@property
	def docker_url_psycopg2(self):
		return f'postgresql+psycopg2://{self.PGUSER}:{self.PGPASS}@{self.PGHOSTDOCKER}:{self.PGPORTDOCKER}/{self.DBNAME}'


settings = Settings()
async_engine = create_async_engine(url=settings.docker_url_asyncpg, echo=True, pool_size=5, max_overflow=10)
async_session_factory = async_sessionmaker(async_engine)
sync_engine = create_engine(settings.docker_url_psycopg2, pool_size=5, max_overflow=10, echo=True)
sync_session_factory = sessionmaker(sync_engine)


class Base(AsyncAttrs, DeclarativeBase):
	"""Base class от которого наследуются остальные"""
	id: Mapped[int] = mapped_column(primary_key=True)
	description: Mapped[str | None]
	created_at: Mapped[datetime] = mapped_column(server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())

	repr_cols_num = 4	  # количество колонок в выводе в принт
	repr_cols = tuple()  # Всё это можно переопределить для подчинённого класса

	def __repr__(self):  # Модифицируем вывод в принт, когда запросы делаем
		"""relationship() не используются в repr. тк могут привести к неожиданным подгрузкам"""
		cols = [f"{col}={getattr(self, col)}" for idx, col in enumerate(self.__table__.columns.keys()) if
				col in self.repr_cols or idx < self.repr_cols_num]

		return f"<{self.__class__.__name__} | {', '.join(cols)} >"
