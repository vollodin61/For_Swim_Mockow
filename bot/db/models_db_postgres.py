import enum
from datetime import datetime
from typing import Optional, Dict

from sqlalchemy import (BigInteger, Integer, String, Column, DateTime, ForeignKey,
						Text, Boolean, MetaData, func, UniqueConstraint)
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from bot.db.db_cfg import Base

matadata_obj = MetaData()


class User(Base):
	__tablename__ = "user"
	tg_id: Mapped[int | None] = mapped_column(BigInteger, unique=True)
	username: Mapped[str | None]
	status: Mapped[str | None]
	first_name: Mapped[str | None]
	last_name: Mapped[str | None]

	# products: Mapped[list["Product"]] = relationship(back_populates="users", secondary="users_products")
# 	club: Mapped[list["Club"]] = relationship(back_populates="users", secondary="clubs_users")
# 	webinars: Mapped[list["Webinar"]] = relationship(back_populates="users", secondary="webinars_users")
# 	polls: Mapped[list["Poll"]] = relationship(back_populates="users", secondary="user_poll")
# 	otz: Mapped[list["Otz"]] = relationship(back_populates="users", secondary="otzs_users")


# class VideoFrom(enum.Enum):
# 	course = "course"
# 	webinar = "webinar"


# class Product(Base):
# 	__tablename__ = 'product'
# 	name: Mapped[str] = mapped_column(unique=True)
# 	# user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
# 	users: Mapped[list["User"]] = relationship(back_populates="products", secondary="users_products")
# 	short_description: Mapped[str | None]


# class UserProduct(Base):
# 	__tablename__ = 'users_products'
# 	user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
# 	product_name: Mapped[str] = mapped_column(ForeignKey('product.name', ondelete='CASCADE'))
# 	UniqueConstraint('user_id', name='idx_users_products')
# user_tg_id: Mapped[int] = mapped_column(ForeignKey('user.tg_id', ondelete="RESTRICT"), nullable=True)
# user = relationship('User', back_populates='course')  # orders = relationship('Order', back_populates='courses')


# class Video(Base):
# 	__tablename__ = 'video'
# 	name: Mapped[str] = mapped_column(unique=True)
# 	url: Mapped[str] = mapped_column(unique=True)
	# webinar: Mapped[str] = mapped_column(ForeignKey('webinars.name', ondelete='CASCADE'), nullable=True)
	# course: Mapped[str] = mapped_column(ForeignKey('course.name', ondelete='CASCADE'), nullable=True)


# class Order(Base):
# 	__tablename__ = 'order'
