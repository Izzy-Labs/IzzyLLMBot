from aioredis import Redis, ConnectionPool
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.misc.env import RedisEnv


class RedisMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()
        redis_url = f"redis://{RedisEnv.USER}:{RedisEnv.PASSWORD}@{RedisEnv.HOST}:{RedisEnv.PORT}"
        self.pool = ConnectionPool.from_url(redis_url, max_connections=10)
        self.redis = Redis(connection_pool=self.pool)

    async def on_pre_process_message(self, message, data: dict):
        message.redis = self.redis
