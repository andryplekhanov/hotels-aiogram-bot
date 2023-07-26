from tgbot.config import Config


def make_connection_string(config: Config) -> str:
    """
    Функция формирует строку для соединения с БД
    """

    return (
        f"postgresql+asyncpg://{config.db.user}:{config.db.password}@"
        f"{config.db.host}:{config.db.port}/{config.db.name}"
    )
