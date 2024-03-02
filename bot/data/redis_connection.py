from redis.asyncio.client import Redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError

RETRY = 3
TIMEOUT = 2


class Singleton:
	"""Эта волшебная штука делает подключение к Redis"""
	_instance = None

	@staticmethod
	def get_connection(host: str):
		if not Singleton._instance:
			Singleton._instance = Redis(host=host, port=6379, socket_timeout=TIMEOUT,
										retry=Retry(ExponentialBackoff(), RETRY),
										retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError])
		return Singleton._instance
