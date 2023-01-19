from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from package.config import config

TORTOISE_ORM = {
    "connections": {"default": config.db.connection_string},
    "apps": {
        "models": {
            "models": [
                "package.db.models.Chat",
                "package.db.models.Message",
                "package.db.models.ChatParticipant",
                "package.db.models.User",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}


def register_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
