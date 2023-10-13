from aiogram import types
from psycopg2 import pool as pg_pool
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.misc.env import PostgresEnv


class DatabaseMiddleware(BaseMiddleware):
    """
    This middleware is used to connect to the database.
    """

    def __init__(self):
        super().__init__()
        self.conn_pool = pg_pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            database=PostgresEnv.DB_NAME,
            user=PostgresEnv.USER,
            password=PostgresEnv.PASSWORD,
            host=PostgresEnv.HOST,
            port=PostgresEnv.PORT
        )

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        """
        This method is called before processing the message.
        :param message:
        :return:
        """
        print(data)
        conn = self.conn_pool.getconn()
        message.data = {'conn': conn}

    async def on_post_process_message(self, message: types.Message, result, data: dict) -> None:
        """
        This method is called after processing the message.
        :param message:
        :return:
        """

        conn = message.data.pop('conn', None)
        if conn:
            self.conn_pool.putconn(conn)
