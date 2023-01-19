import uvicorn
from fastapi import FastAPI

from package.config import config
from package.db import register_db
from package.exceptions.CustomException import (
    CustomException,
    custom_exceptions_handler,
)

# from package.routes.chat import router as chat_router
from package.routes.user import router as user_router

app = FastAPI()
app.include_router(user_router)
# app.include_router(chat_router)

if __name__ == "__main__":
    register_db(app)
    app.add_exception_handler(CustomException, custom_exceptions_handler)

    uvicorn.run(
        app,
        host=config.address.host,
        port=config.address.port
    )
