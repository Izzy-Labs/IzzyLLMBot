from os import environ
from dotenv import load_dotenv

load_dotenv()


class TgKey:
    TOKEN: str = environ.get("TG_BOT_TOKEN", "define me")
    