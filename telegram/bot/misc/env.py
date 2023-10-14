from os import environ


class TgKey:
    TOKEN: str = environ.get("TG_BOT_TOKEN", "define me")


class PostgresEnv:
    HOST: str = environ.get("POSTGRES_HOST", "define me")
    PORT: int = int(environ.get("POSTGRES_PORT", "define me"))
    USER: str = environ.get("POSTGRES_USER", "define me")
    PASSWORD: str = environ.get("POSTGRES_PASSWORD", "define me")
    DB_NAME: str = environ.get("POSTGRES_DB", "define me")


class RedisEnv:
    HOST: str = environ.get("REDIS_HOST", "define me")
    PORT: int = int(environ.get("REDIS_PORT", "define me"))
    DB: int = int(environ.get("REDIS_DB", "define me"))
    USER: str = environ.get("REDIS_USER", "define me")
    PASSWORD: str | None = environ.get("REDIS_PASSWORD", None)
