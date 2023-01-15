import uvicorn
from fastapi import FastAPI

from package.config import config
from package.db import register_db
from package.routes.user import router as user_router

app = FastAPI()
app.include_router(user_router)

if __name__ == "__main__":
    register_db(app)

    uvicorn.run(
        app,
        host=config.address.host,
        port=config.address.port
    )
