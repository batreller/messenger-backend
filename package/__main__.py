import uvicorn
from fastapi import FastAPI

from package.config import config
from package.db import register_db
from package.exceptions.CustomException import (
    CustomException,
    custom_exceptions_handler,
)
from package.routes import auth, chat, message, user

app = FastAPI()
app.add_exception_handler(CustomException, custom_exceptions_handler)

register_db(app)

for route_module in [user, auth, chat, message]:
    app.include_router(route_module.router)


if __name__ == "__main__":
    uvicorn.run(
        'package.__main__:app',
        host=config.address.host,
        port=config.address.port,
        reload=True
    )
