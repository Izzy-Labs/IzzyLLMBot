from aioredis import Redis, ConnectionPool
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.misc.env import RedisEnv


class RedisMiddleware(BaseMiddleware):
    """
    Middleware for adding redis connection to message
    """
    def __init__(self):
        super().__init__()
        redis_url = f"redis://{RedisEnv.USER}:{RedisEnv.PASSWORD}@{RedisEnv.HOST}:{RedisEnv.PORT}"
        self.pool = ConnectionPool.from_url(redis_url, max_connections=10)
        self.redis = Redis(connection_pool=self.pool)

    async def on_pre_process_message(self, message, data: dict) -> None:
        """
        Add redis connection to message
        :param message:
        :param data:
        :return:
        """
        message.redis = self.redis

    async def on_pre_process_callback_query(self, callback_query, data: dict) -> None:
        """
        Add redis connection to callback_query
        :param callback_query:
        :param data:
        :return:
        """
        callback_query.redis = self.redis
